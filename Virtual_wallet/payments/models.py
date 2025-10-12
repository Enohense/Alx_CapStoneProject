from django.db import models
from wallets.models import Wallet
from transactions.models import Transaction
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Payment(models.Model):
    """
    External payment processing (deposits via payment gateway)
    """
    PAYMENT_METHODS = [
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CARD', 'Card'),
        ('USSD', 'USSD'),
        ('BANK_ACCOUNT', 'Bank Account'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
        ('EXPIRED', 'Expired'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=100, unique=True, db_index=True)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    # Paystack, Flutterwave, etc.
    provider = models.CharField(max_length=50, default='Paystack')
    provider_reference = models.CharField(
        max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='PENDING')
    webhook_received = models.BooleanField(default=False)
    webhook_data = models.JSONField(blank=True, null=True)
    initiated_at = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.reference} - {self.amount} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.reference:
            import time
            self.reference = f"PAY_{int(time.time())}{str(uuid.uuid4())[:8]}"
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-initiated_at']
