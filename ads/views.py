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
from django.db.models import Q
from common.utils import paginate_and_filter_queryset
logger = logging.getLogger(__name__)


class GetCategoryList(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        try:
            categories = Category.objects.active()
            return paginate_and_filter_queryset(
                request,
                categories,
                self.serializer_class,
                search_fields=['name', 'display_name'],
                ordering_fields=['order', 'name']
            )
        except Exception as e:
            logger.error(f"Error fetching category list: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while fetching categories.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSubCategoryList(APIView):
    serializer_class = SubCategorySerializer

    def get(self, request):
        try:
            sub_categories = SubCategory.objects.active()
            return paginate_and_filter_queryset(
                request,
                sub_categories,
                self.serializer_class,
                search_fields=['name', 'display_name', 'category__name'],
                ordering_fields=['order', 'name']
            )
        except Exception as e:
            logger.error(f"Error fetching subcategory list: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while fetching subcategories.",
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

            # Filter by location
            location = request.query_params.get('location')
            if location:
                ads = ads.filter(location__icontains=location)

            # Save search history if authenticated
            if request.user.is_authenticated:
                query = request.query_params.get('search')
                if query:
                    SearchHistory.objects.create(user=request.user, query=query)

            return paginate_and_filter_queryset(
                request,
                ads,
                self.serializer_class,
                search_fields=['title', 'description', 'location'],
                ordering_fields=['created_at', 'price']
            )
        except Exception as e:
            logger.error(f"Error while fetching ads: {e}")
            return Response({
                "status": False,
                "message": "An error occurred fetching ads.",
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
            serializer = self.serializer_class(user_ads, many=True)
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
    serializer_class = FavoriteAdSerializer

    def get(self, request):
        try:
            favorites = FavoriteAd.objects.for_user(request.user)
            serializer = self.serializer_class(favorites, many=True)
            return Response({
                "status": True,
                "favourites":  serializer.data},
                status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error while fetching list of favourite ads: {e}")
            return Response({
                "status": False,
                "message": "An error occurred fetching list of favourite ads.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ad_id):
        try:
            ad = Ad.objects.active().get(id=ad_id)  # Use your custom manager if you have one
        except Ad.DoesNotExist:
            return Response(
                {"message": "Ad not found or is no longer active."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            favorite, created = FavoriteAd.objects.get_or_create(user=request.user, ad=ad)
            if created:
                return Response({'message': 'Ad added to favorites.'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'Already in favorites.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error while adding to favorites: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while adding to favorites.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveFromFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, ad_id):
        try:
            favorite = FavoriteAd.objects.for_user(request.user).filter(ad__id=ad_id).first()
            if favorite:
                favorite.delete()
                return Response({'message': 'Ad removed from favorites.'}, status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Favorite not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error while removing from favorites: {e}")
            return Response({
                "status": False,
                "message": "An error occurred while removing from favorites.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FilteredAdListView(APIView):
    serializer_class = AdListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Ad.objects.active().order_recent()

        # Search
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )

        # Sort by
        sort_by = self.request.query_params.get('sort_by')
        if sort_by in ['price', '-price', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)

        # Filter by location
        location = self.request.query_params.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)

        return queryset


class UserSearchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            history = SearchHistory.objects.filter(user=request.user)
            data = [{"query": h.query, "searched_at": h.searched_at} for h in history]
            return Response({"status": True, "history": data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching search history: {e}")
            return Response({
                "status": False,
                "message": "Failed to fetch search history",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
