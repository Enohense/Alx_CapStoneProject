from django.db import models
from wallets.models import Wallet
from transactions.models import Transaction
from decimal import Decimal
import uuid


class LedgerEntry(models.Model):
    """
    Immutable audit trail of all balance changes (double-entry bookkeeping)
    """
    ENTRY_TYPES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name='ledger_entries'
    )
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='ledger_entries')
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    balance_before = models.DecimalField(max_digits=15, decimal_places=2)
    balance_after = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.entry_type} - {self.wallet.user.username} - {self.amount}"

    def save(self, *args, **kwargs):
        # Ledger entries are immutable - prevent updates
        if self.pk is not None:
            raise ValueError("Ledger entries cannot be modified once created")
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'ledger_entries'
        verbose_name = 'Ledger Entry'
        verbose_name_plural = 'Ledger Entries'
        ordering = ['-created_at']
