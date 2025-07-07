from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from django.db import transaction
from common.utils import get_serializer_error_as_string
import logging
from rest_framework.permissions import IsAuthenticated
from .models import *

logger = logging.getLogger(__name__)


class GetCategoryList(APIView):
    serializer_class = CategorySerializer

    #permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            categories = Category.objects.active()
            serializer = self.serializer_class(categories, many=True)
            return Response({
                "status": True,
                "message": "Categories fetched successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching category list: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while fetching categories.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSubCategoryList(APIView):
    serializer_class = SubCategorySerializer

    #permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            sub_categories = SubCategory.objects.active()
            serializer = self.serializer_class(sub_categories, many=True)
            return Response({
                "status": True,
                "message": "Sub Categories fetched successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching  sub category list: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while fetching sub categories.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateAdView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdCreateSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({
                    "status": True,
                    "message": "Ad created successfully.",
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response({'error': get_serializer_error_as_string(serializer)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error fetching  error creating ad: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while creating ad.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListAdsView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AdListSerializer

    def get(self, request):
        try:
            ads = Ad.objects.active().order_recent()
            serializer = AdListSerializer(ads, many=True)
            return Response({
                "status": True,
                'ads': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error while fetching list of ads: {e}")
            return Response({
                "status": False,
                "message": "An error occurred fetching list of ads.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AdDetailSerializer

    def get(self, request, id):
        try:
            ad = Ad.objects.active().get(id=id)
        except Ad.DoesNotExist:
            return Response(
                {"message": "Ad not found or is no longer active."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Unexpected error while retrieving ad {id}: {str(e)}")
            return Response(
                {"message": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = self.serializer_class(ad)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAdsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAdListSerializer

    def get(self, request):
        try:
            user_ads = Ad.objects.for_user(request.user).order_recent()
            serializer = UserAdListSerializer(user_ads, many=True)
            return Response({
                "status": True,
                'user_ads': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error while fetching list of user's ads: {e}")
            return Response({
                "status": False,
                "message": "An error occurred fetching list of user's ads.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavoriteAdsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = FavoriteAd.objects.for_user(request.user)
        serializer = FavoriteAdSerializer(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ad_id):
        ad = get_object_or_404(Ad, id=ad_id)
        favorite, created = FavoriteAd.objects.get_or_create(user=request.user, ad=ad)
        if created:
            return Response({'message': 'Ad added to favorites.'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Already in favorites.'}, status=status.HTTP_200_OK)


class RemoveFromFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, ad_id):
        favorite = FavoriteAd.objects.filter(user=request.user, ad__id=ad_id).first()
        if favorite:
            favorite.delete()
            return Response({'message': 'Ad removed from favorites.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)
