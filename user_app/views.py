from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User
from .serializers import UserSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
# User Registration View
class RegisterView(APIView):
    @swagger_auto_schema(
        operation_id="Register User",
        operation_description="API to register a new user.",
        request_body=UserSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully.",
                examples={
                    "application/json": {
                        "message": "User registered successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Validation errors occurred.",
                examples={
                    "application/json": {
                        "email": ["This field is required."],
                        "password": ["This field is required."]
                    }
                }
            ),
            500: openapi.Response(
                description="Server error.",
                examples={
                    "application/json": {
                        "message": "Error: <error_details>"
                    }
                }
            ),
        }
    )
    def post(self, request):
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
    @swagger_auto_schema(
        operation_id="User Login",
        operation_description="API to authenticate user and generate JWT tokens.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            },
            required=['email', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful. Tokens generated.",
                examples={
                    "application/json": {
                        "refresh": "<refresh_token>",
                        "access": "<access_token>"
                    }
                }
            ),
            401: openapi.Response(
                description="Invalid credentials.",
                examples={
                    "application/json": {
                        "message": "Invalid credentials"
                    }
                }
            ),
            404: openapi.Response(
                description="User not found.",
                examples={
                    "application/json": {
                        "message": "User not found"
                    }
                }
            ),
            500: openapi.Response(
                description="Server error.",
                examples={
                    "application/json": {
                        "message": "Error: <error_details>"
                    }
                }
            ),
        }
    )
    def post(self, request):
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
    @swagger_auto_schema(
        operation_id="User Logout",
        operation_description="API to logout a user by blacklisting their refresh token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            },
            required=['refresh']
        ),
        responses={
            200: openapi.Response(
                description="Logout successful.",
                examples={
                    "application/json": {
                        "message": "Logout successful"
                    }
                }
            ),
            400: openapi.Response(
                description="Refresh token is missing.",
                examples={
                    "application/json": {
                        "message": "Refresh token is required"
                    }
                }
            ),
            500: openapi.Response(
                description="Server error.",
                examples={
                    "application/json": {
                        "message": "Error: <error_details>"
                    }
                }
            ),
        }
    )
    def post(self, request):
        try:
            token = request.data.get('refresh')
            if not token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            refresh_token = RefreshToken(token)
            refresh_token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)