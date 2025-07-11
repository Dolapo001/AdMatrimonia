from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import MatrimonyProfile
from .serializers import MatrimonyProfileSerializer
import logging

logger = logging.getLogger(__name__)


class GetProfileVIew(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def get(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if not profile:
                return Response({
                    "status": False,
                    "message": "User profile not found"
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(profile)
            return Response({
                "status": True,
                "message": "User profile fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching user's profile: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while fetching user's profile.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    "status": True,
                    "message": "User profile created successfully",
                    "data": serializer.data
                    }, status=status.HTTP_201_CREATED)
            return Response({
                "status": False,
                "message": "An error occurred"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error creating user's profile: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while creating user's profile.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



