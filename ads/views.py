from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import *
from django.db import transaction
from common.utils import get_serializer_error_as_string
import logging
from .models import *
from django.db.models import Q
from common.utils import paginate_and_filter_queryset
from common.response_managers import *
from django.db import transaction

logger = logging.getLogger(__name__)


class GetCategoryList(APIView):
    serializer_class = CategorySerializer

    def get(self, request):
        try:
            categories = Category.objects.active()
            return ResponseManager.custom_paginated_response(
                request,
                categories,
                self.serializer_class,
                search_fields=['name', 'display_name'],
                ordering_fields=['order', 'name'],
                message=ResponseStatus.CATEGORIES_FETCHED
            )
        except Exception as e:
            return ResponseManager.server_error_response(
                message="Failed to fetch categories",
                error=str(e)
            )


class GetSubCategoryList(APIView):
    serializer_class = SubCategorySerializer

    def get(self, request):
        try:
            sub_categories = SubCategory.objects.active()
            return ResponseManager.custom_paginated_response(
                request,
                sub_categories,
                self.serializer_class,
                search_fields=['name', 'display_name', 'category__name'],
                ordering_fields=['order', 'name'],
                message=ResponseStatus.SUBCATEGORIES_FETCHED
            )
        except Exception as e:
            return ResponseManager.server_error_response(
                message="Failed to fetch subcategories",
                error=str(e)
            )


class CreateAdView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdCreateSerializer

    @transaction.atomic()
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return ResponseManager.validation_error_response(
                    message=ResponseStatus.VALIDATION_FAILED,
                    errors=get_serializer_error_as_string(serializer)
                )

            with transaction.atomic():
                serializer.save(user=request.user)

            return ResponseManager.created_response(
                message=ResponseStatus.AD_CREATED,
                data=serializer.data
            )
        except Exception as e:
            logger.exception("Ad creation failed")
            return ResponseManager.server_error_response(
                message="Failed to create ad",
                error=str(e)
            )


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
                    try:
                        SearchHistory.objects.create(user=request.user, query=query)
                    except Exception as e:
                        logger.error(f"Failed to save search history: {str(e)}")

            return ResponseManager.custom_paginated_response(
                request,
                ads,
                self.serializer_class,
                search_fields=['title', 'description', 'location'],
                ordering_fields=['created_at', 'price'],
                message=ResponseStatus.ADS_FETCHED
            )
        except Exception as e:
            logger.exception("Failed to list ads")
            return ResponseManager.server_error_response(
                message="Failed to fetch ads",
                error=str(e)
            )


class AdDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class = AdDetailSerializer

    def get(self, request, id):
        try:
            ad = Ad.objects.active().get(id=id)
            serializer = self.serializer_class(ad)
            return ResponseManager.success_response(
                message=ResponseStatus.AD_FETCHED,
                data=serializer.data
            )
        except Ad.DoesNotExist:
            return ResponseManager.not_found_response(ResponseStatus.AD_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Failed to fetch ad {id}")
            return ResponseManager.server_error_response(
                message="Failed to fetch ad details",
                error=str(e)
            )


class UserAdsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserAdListSerializer

    def get(self, request):
        try:
            user_ads = Ad.objects.for_user(request.user).order_recent()
            serializer = self.serializer_class(user_ads, many=True)
            return ResponseManager.success_response(
                message=ResponseStatus.USER_ADS_FETCHED,
                data={"user_ads": serializer.data}
            )
        except Exception as e:
            logger.exception("Failed to fetch user ads")
            return ResponseManager.server_error_response(
                message="Failed to fetch user ads",
                error=str(e)
            )


class FavoriteAdsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteAdSerializer

    def get(self, request):
        try:
            favorites = FavoriteAd.objects.for_user(request.user)
            serializer = self.serializer_class(favorites, many=True)
            return ResponseManager.success_response(
                message=ResponseStatus.FAVORITE_ADS_FETCHED,
                data={"favourites": serializer.data}
            )
        except Exception as e:
            logger.exception("Failed to fetch favorite ads")
            return ResponseManager.server_error_response(
                message="Failed to fetch favorites",
                error=str(e)
            )


class AddToFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def post(self, request, ad_id):
        try:
            ad = Ad.objects.active().get(id=ad_id)
        except Ad.DoesNotExist:
            return ResponseManager.not_found_response(ResponseStatus.AD_NOT_FOUND)
        except Exception as e:
            return ResponseManager.server_error_response(
                message="Failed to fetch ad",
                error=str(e)
            )

        try:
            favorite, created = FavoriteAd.objects.get_or_create(user=request.user, ad=ad)
            if created:
                return ResponseManager.created_response(ResponseStatus.AD_ADDED_TO_FAVORITES)
            return ResponseManager.success_response(ResponseStatus.AD_ALREADY_IN_FAVORITES)
        except Exception as e:
            logger.exception("Failed to add favorite")
            return ResponseManager.server_error_response(
                message="Failed to add to favorites",
                error=str(e)
            )


class RemoveFromFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic()
    def delete(self, request, ad_id):
        try:
            favorite = FavoriteAd.objects.for_user(request.user).filter(ad__id=ad_id).first()
            if not favorite:
                return ResponseManager.not_found_response(ResponseStatus.FAVORITE_NOT_FOUND)

            favorite.delete()
            return ResponseManager.deleted_response(ResponseStatus.AD_REMOVED_FROM_FAVORITES)
        except Exception as e:
            logger.exception("Failed to remove favorite")
            return ResponseManager.server_error_response(
                message="Failed to remove from favorites",
                error=str(e)
            )


class FilteredAdListView(APIView):
    serializer_class = AdListSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            queryset = Ad.objects.active().order_recent()

            # Apply filters
            search = request.query_params.get('search')
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(description__icontains=search) |
                    Q(location__icontains=search)
                )

            # Apply sorting
            sort_by = request.query_params.get('sort_by')
            if sort_by in ['price', '-price', 'created_at', '-created_at']:
                queryset = queryset.order_by(sort_by)

            # Filter by location
            location = request.query_params.get('location')
            if location:
                queryset = queryset.filter(location__icontains=location)

            return ResponseManager.custom_paginated_response(
                request,
                queryset,
                self.serializer_class,
                search_fields=['title', 'description', 'location'],
                ordering_fields=['created_at', 'price'],
                message=ResponseStatus.ADS_FETCHED
            )
        except Exception as e:
            logger.exception("Failed to filter ads")
            return ResponseManager.server_error_response(
                message="Failed to filter ads",
                error=str(e)
            )


class UserSearchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            history = SearchHistory.objects.filter(user=request.user).order_by('-searched_at')
            data = [{"query": h.query, "searched_at": h.searched_at} for h in history]
            return ResponseManager.success_response(
                message=ResponseStatus.SEARCH_HISTORY_FETCHED,
                data={"history": data}
            )
        except Exception as e:
            logger.exception("Failed to fetch search history")
            return ResponseManager.server_error_response(
                message="Failed to fetch search history",
                error=str(e)
            )