from django.db import models
from django.contrib.auth.models import User
from wallets.models import Wallet
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Transaction(models.Model):
    """
    All wallet transactions (deposits, withdrawals, transfers)
    """
    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAWAL', 'Withdrawal'),
        ('TRANSFER_OUT', 'Transfer Out'),
        ('TRANSFER_IN', 'Transfer In'),
        ('REVERSAL', 'Reversal'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REVERSED', 'Reversed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=100, unique=True, db_index=True)
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(
        max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    currency = models.CharField(max_length=3, default='NGN')
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='PENDING')
    description = models.TextField(blank=True, null=True)

    # For transfers
    recipient_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='received_transactions'
    )

    # For withdrawals
    recipient_account = models.CharField(max_length=10, blank=True, null=True)
    recipient_bank = models.CharField(max_length=100, blank=True, null=True)

    # For external payments
    payment_reference = models.CharField(max_length=255, blank=True, null=True)

    # Idempotency
    idempotency_key = models.CharField(
        max_length=255, unique=True, blank=True, null=True)

    # Metadata
    metadata = models.JSONField(blank=True, null=True)

    # Timestamps
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference} - {self.transaction_type} - {self.currency} {self.amount}"

    def save(self, *args, **kwargs):
        if not self.reference:
            # Auto-generate reference
            prefix = self.transaction_type[:3].upper()
            import time
            self.reference = f"TXN_{prefix}_{int(time.time())}{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'transactions'
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status']),
            models.Index(fields=['transaction_type']),
            models.Index(fields=['-created_at']),
        ]
