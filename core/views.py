from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.db import transaction
from common.utils import get_serializer_error_as_string
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainSerializer

logger = logging.getLogger(__name__)


class RegistrationView(APIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  # This returns a User instance

                # Double-check that we have a User instance
                if not isinstance(user, User):
                    raise ValueError(f"Expected User instance, got {type(user)}")

                return Response(
                    {"id": user.id, "message": "User registered successfully"},
                    status=status.HTTP_201_CREATED,
                )

            return Response(
                {
                    "message": get_serializer_error_as_string(serializer.errors),
                    "data": None,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            return Response(
                {"message": f"Internal Server Error: {str(e)}", "data": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data.get("user")

                if not user:
                    return Response(
                        {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
                    )

                refresh = RefreshToken.for_user(user)
                access = (
                    refresh.access_token
                )

                tokens = {"refresh": str(refresh), "access": str(access)}
                return Response(tokens, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error occurred during login: {e}")
            return Response(
                {"message": "Internal Server Error", "data": None},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

