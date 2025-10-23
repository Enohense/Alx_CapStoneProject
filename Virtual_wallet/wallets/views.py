from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import WalletSerializer


class WalletDetailView(generics.RetrieveAPIView):
    """
    Get authenticated user's wallet details
    """
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet


class WalletBalanceView(APIView):
    """
    Quick balance check endpoint
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = request.user.wallet

        return Response({
            'wallet_id': str(wallet.id),
            'available_balance': str(wallet.balance),
            'pending_balance': str(wallet.pending_balance),
            'total_balance': str(wallet.total_balance),
            'currency': wallet.currency,
            'formatted': {
                'available': f'₦{wallet.balance:,.2f}',
                'pending': f'₦{wallet.pending_balance:,.2f}',
                'total': f'₦{wallet.total_balance:,.2f}'
            }
        })
