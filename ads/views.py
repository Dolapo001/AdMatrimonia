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
            categories = Category.objects.filter(is_active=True).order_by('order')
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
            sub_categories = SubCategory.objects.filter(is_active=True).order_by('order')
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

