from wallets.models import Wallet
from rest_framework import serializers
from .models import Transaction
from django.contrib.auth.models import User


class TransactionSerializer(serializers.ModelSerializer):
    wallet_user = serializers.CharField(
        source='wallet.user.username', read_only=True)
    recipient_username = serializers.CharField(
        source='recipient_wallet.user.username', read_only=True, allow_null=True)

    class Meta:
        model = Transaction
        fields = [
            'id', 'reference', 'wallet_user', 'transaction_type', 'amount',
            'currency', 'status', 'description', 'recipient_username',
            'recipient_account', 'recipient_bank', 'payment_reference',
            'initiated_at', 'completed_at', 'created_at'
        ]
        read_only_fields = ['id', 'reference', 'status', 'initiated_at',
                            'completed_at', 'created_at']


class TransferSerializer(serializers.Serializer):
    recipient_username = serializers.CharField(max_length=150)
    amount = serializers.DecimalField(
        max_digits=15, decimal_places=2, min_value=0.01)
    description = serializers.CharField(
        max_length=255, required=False, allow_blank=True)
    transaction_pin = serializers.CharField(
        max_length=4, write_only=True, required=False)

    def validate_recipient_username(self, value):
        """Check if recipient exists"""
        try:
            user = User.objects.get(username=value)
            # Check if user has a wallet
            if not hasattr(user, 'wallet'):
                raise serializers.ValidationError(
                    "Recipient does not have a wallet")
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User '{value}' not found")
        return value

    def validate(self, data):
        """Additional validations"""
        request = self.context.get('request')

        # Prevent self-transfer
        if data['recipient_username'] == request.user.username:
            raise serializers.ValidationError("Cannot transfer to yourself")

        # Check if sender has sufficient balance
        sender_wallet = request.user.wallet
        if sender_wallet.balance < data['amount']:
            raise serializers.ValidationError({
                'amount': f"Insufficient balance. Available: ₦{sender_wallet.balance:,.2f}"
            })

        return data
