from django.urls import path
from .views import WalletDetailView, WalletBalanceView

urlpatterns = [
    path('', WalletDetailView.as_view(), name='wallet-detail'),
    path('balance/', WalletBalanceView.as_view(), name='wallet-balance'),
]
