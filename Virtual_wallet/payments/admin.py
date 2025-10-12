from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reference', 'wallet', 'amount',
                    'payment_method', 'status', 'initiated_at']
    list_filter = ['payment_method', 'status', 'initiated_at']
    search_fields = ['reference', 'wallet__user__username']
    readonly_fields = ['id', 'reference', 'initiated_at', 'confirmed_at']
