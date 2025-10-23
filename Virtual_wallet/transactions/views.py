from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db import transaction as db_transaction
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

from .models import Transaction
from .serializers import TransactionSerializer, TransferSerializer
from wallets.models import Wallet
from ledger.models import LedgerEntry


class TransactionListView(generics.ListAPIView):
    """
    List all transactions for authenticated user with filtering
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Transaction.objects.filter(wallet=self.request.user.wallet)

        # Filter by type
        transaction_type = self.request.query_params.get('type', None)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        # Filter by status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-created_at')


class TransactionDetailView(generics.RetrieveAPIView):
    """
    Get details of a specific transaction
    """
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet=self.request.user.wallet)


class TransferView(APIView):
    """
    Transfer money to another user
    """
    permission_classes = [IsAuthenticated]

    @db_transaction.atomic
    def post(self, request):
        serializer = TransferSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Get sender and recipient
        sender = request.user
        sender_wallet = Wallet.objects.select_for_update().get(user=sender)

        recipient_username = serializer.validated_data['recipient_username']
        recipient = User.objects.get(username=recipient_username)
        recipient_wallet = Wallet.objects.select_for_update().get(user=recipient)

        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get(
            'description', f'Transfer to {recipient_username}')

        # Check wallet status
        if sender_wallet.status != 'ACTIVE':
            return Response({
                'error': 'WALLET_NOT_ACTIVE',
                'message': f'Your wallet is {sender_wallet.status}. Cannot process transfer.'
            }, status=status.HTTP_403_FORBIDDEN)

        if recipient_wallet.status != 'ACTIVE':
            return Response({
                'error': 'RECIPIENT_WALLET_NOT_ACTIVE',
                'message': 'Recipient wallet is not active'
            }, status=status.HTTP_403_FORBIDDEN)

        # Double-check balance (redundant but safe)
        if sender_wallet.balance < amount:
            return Response({
                'error': 'INSUFFICIENT_BALANCE',
                'message': f'Insufficient balance. Available: ₦{sender_wallet.balance:,.2f}'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create transfer-out transaction for sender
        transfer_out = Transaction.objects.create(
            wallet=sender_wallet,
            transaction_type='TRANSFER_OUT',
            amount=amount,
            currency=sender_wallet.currency,
            status='COMPLETED',
            description=description,
            recipient_wallet=recipient_wallet,
            completed_at=timezone.now()
        )

        # Create transfer-in transaction for recipient
        transfer_in = Transaction.objects.create(
            wallet=recipient_wallet,
            transaction_type='TRANSFER_IN',
            amount=amount,
            currency=recipient_wallet.currency,
            status='COMPLETED',
            description=f'Transfer from {sender.username}',
            completed_at=timezone.now()
        )

        # Update balances
        sender_balance_before = sender_wallet.balance
        sender_wallet.balance -= amount
        sender_wallet.save()

        recipient_balance_before = recipient_wallet.balance
        recipient_wallet.balance += amount
        recipient_wallet.save()

        # Create ledger entries (audit trail)
        # Debit sender
        LedgerEntry.objects.create(
            transaction=transfer_out,
            wallet=sender_wallet,
            entry_type='DEBIT',
            amount=amount,
            balance_before=sender_balance_before,
            balance_after=sender_wallet.balance,
            description=f'Transfer to {recipient_username}: {description}'
        )

        # Credit recipient
        LedgerEntry.objects.create(
            transaction=transfer_in,
            wallet=recipient_wallet,
            entry_type='CREDIT',
            amount=amount,
            balance_before=recipient_balance_before,
            balance_after=recipient_wallet.balance,
            description=f'Transfer from {sender.username}: {description}'
        )

        return Response({
            'transaction': TransactionSerializer(transfer_out).data,
            'balance_update': {
                'previous_balance': str(sender_balance_before),
                'new_balance': str(sender_wallet.balance),
                'currency': sender_wallet.currency
            },
            'message': 'Transfer successful'
        }, status=status.HTTP_201_CREATED)
