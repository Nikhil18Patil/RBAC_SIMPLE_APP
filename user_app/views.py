from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User
from .serializers import UserSerializer

# User Registration View
class RegisterView(APIView):
    def post(self, request):
        """
        Handles user registration.
        """
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Login View
class LoginView(APIView):
    def post(self, request):
        """
        Handles user login and JWT token generation.
        """
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
           
            user = User.objects.get(email=email)
            if not user.check_password(password):
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            
            
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User Logout View
class LogoutView(APIView):
    def post(self, request):
        """
        Handles user logout by blacklisting the refresh token.
        """
        try:
            
            token = request.data.get('refresh')
            if not token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
