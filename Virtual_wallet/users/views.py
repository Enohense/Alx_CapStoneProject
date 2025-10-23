from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a new user and automatically create wallet
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'wallet': {
                'id': str(user.wallet.id),
                'balance': str(user.wallet.balance),
                'currency': user.wallet.currency,
                'status': user.wallet.status
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            'message': 'Registration successful. Your wallet has been created.'
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Login and get JWT tokens
    """
    permission_classes = [AllowAny]

    def get(self, request):  # ADD THIS METHOD
        """For DRF browsable API"""
        return Response({
            'message': 'Send POST request with username and password'
        })

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({
                'error': 'Account is disabled'
            }, status=status.HTTP_403_FORBIDDEN)

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'wallet': {
                'balance': str(user.wallet.balance),
                'currency': user.wallet.currency
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update user profile
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
