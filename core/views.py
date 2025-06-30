from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.db import transaction
from common.utils import get_serializer_error_as_string
import logging
from rest_framework.permissions import IsAuthenticated


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
