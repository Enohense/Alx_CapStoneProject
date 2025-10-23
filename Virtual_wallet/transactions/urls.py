from django.urls import path
from .views import TransactionListView, TransactionDetailView, TransferView

urlpatterns = [
    path('', TransactionListView.as_view(), name='transaction-list'),
    path('<uuid:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('transfer/', TransferView.as_view(), name='transfer'),
]
