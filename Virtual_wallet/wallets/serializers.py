from rest_framework import serializers
from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    total_balance = serializers.DecimalField(
        max_digits=15,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'balance', 'pending_balance', 'total_balance',
                  'currency', 'status', 'daily_limit', 'created_at', 'updated_at']
        read_only_fields = ['id', 'balance', 'pending_balance', 'created_at',
                            'updated_at', 'user']
