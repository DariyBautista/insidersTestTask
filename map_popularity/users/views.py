from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .utils import generate_random_password, send_password_reset_email

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Successfully logged in."}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.set_password(new_password)
            user.save()
            send_password_reset_email(user, new_password)
            return Response({"message": "Password reset successfully. Please check your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "No user found with this email address."}, status=status.HTTP_400_BAD_REQUEST)
