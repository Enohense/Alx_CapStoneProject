from django.contrib import admin
from .models import LedgerEntry


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ['wallet', 'entry_type', 'amount',
                    'balance_before', 'balance_after', 'created_at']
    list_filter = ['entry_type', 'created_at']
    search_fields = ['wallet__user__username', 'transaction__reference']
    readonly_fields = ['id', 'transaction', 'wallet', 'entry_type',
                       'amount', 'balance_before', 'balance_after', 'created_at']

    # Make ledger entries read-only
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
