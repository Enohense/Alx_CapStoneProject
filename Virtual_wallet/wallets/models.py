from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Wallet(models.Model):
    """
    Digital wallet for each user
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('FROZEN', 'Frozen'),
        ('CLOSED', 'Closed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    pending_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    currency = models.CharField(max_length=3, default='NGN')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    daily_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet - {self.currency} {self.balance}"

    @property
    def total_balance(self):
        """Total balance including pending"""
        return self.balance + self.pending_balance

    class Meta:
        db_table = 'wallets'
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'


# Signal to automatically create Wallet when User is created


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
