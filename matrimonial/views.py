from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
import logging

logger = logging.getLogger(__name__)


class GetProfileView(APIView):
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


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def put(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if not profile:
                return Response({
                    "status": False,
                    "message": "User profile not found"
                }, status=status.HTTP_404_NOT_FOUND)
            serializer = self.serializer_class(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": True,
                    "message": "User profile updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "status": False,
                "message": "An error occurred"
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating user's profile: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while updating user's profile.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if profile:
                profile.delete()
                return Response({
                    "status": True,
                    "message": "User profile deleted successfully",
                }, status=status.HTTP_204_NO_CONTENT)
            return Response({
                "status": False,
                "message": "User profile not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error deleting user's profile: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while deleting user's profile.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MatrimonyProfileListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def get(self, request):
        try:
            filters = request.query_params
            queryset = MatrimonyProfile.objects.list_profiles(filters)

            paginator = PageNumberPagination()
            paginator.page_size = 10
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(result_page, many=True)

            return paginator.get_paginated_response({
                "status": True,
                "message": "Profiles fetched successfully",
                "data": serializer.data
            })
        except Exception as e:
            return Response({
                "status": False,
                "message": "Error occurred while listing profiles.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MatrimonyProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(user_id)
            if not profile:
                return Response({
                    "status": False,
                    "message": "Profile not found"
                }, status=status.HTTP_404_NOT_FOUND)

            serializer = MatrimonyProfileSerializer(profile)
            return Response({
                "status": True,
                "message": "Profile fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": "An error occurred while fetching profile",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MatrimonyProfilePicturesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfilePictureSerializer

    def get(self, request, user_id):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(user_id)
            if not profile:
                return Response({
                    "status": False,
                    "message": "Profile not found"
                }, status=status.HTTP_404_NOT_FOUND)

            pictures = profile.pictures.all()
            serializer = self.serializer_class(pictures, many=True)
            return Response({
                "status": True,
                "message": "Pictures fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": False,
                "message": "An error occurred while fetching pictures",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UploadProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfilePictureSerializer

    def post(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if not profile:
                return Response({
                    "status": False,
                    "message": "User profile not found"
                }, status=status.HTTP_404_NOT_FOUND)

            image = request.FILES.get('image')
            if not image:
                return Response({
                    "status": False,
                    "message": "Image is required"
                }, status=status.HTTP_400_BAD_REQUEST)

            picture = profile.pictures.create(image=image)
            serializer = self.serializer_class(picture)
            return Response({
                "status": True,
                "message": "Picture uploaded successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "status": False,
                "message": "An error occurred while uploading picture",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, picture_id):
        try:
            picture = MatrimonyProfilePicture.objects.filter(
                id=picture_id,
                profile__user=request.user
            ).first()

            if not picture:
                return Response({
                    "status": False,
                    "message": "Picture not found or unauthorized"
                }, status=status.HTTP_404_NOT_FOUND)

            picture.delete()
            return Response({
                "status": True,
                "message": "Picture deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({
                "status": False,
                "message": "An error occurred while deleting picture",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


