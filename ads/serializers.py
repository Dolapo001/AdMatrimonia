from rest_framework import serializers
from .models import Category, SubCategory, Ad, FavoriteAd
from core.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name', 'icon', 'color', 'is_active', 'order']


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'display_name', 'is_active', 'order', 'category']


# class AdSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     subcategory = SubCategorySerializer(read_only=True)
#
#     class Meta:
#         model = Ad
#         fields = [
#             'id', 'title', 'description', 'price', 'currency',
#             'location', 'contact_phone', 'contact_email', 'images',
#             'status', 'is_featured', 'is_sold', 'is_expired',
#             'created_at', 'updated_at', 'expires_at', 'publik_id',
#             'category', 'subcategory'
#         ]


class AdCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['subcategory', 'title', 'description', 'category', 'price', 'currency', 'location', 'contact_phone',
                  'contact_email', 'images', 'publik_id']
        read_only_fields = ['publik_id']


class AdDetailSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='user.name')

    class Meta:
        model = Ad
        fields = ['id', 'publik_id', 'title', 'description', 'creator', 'location', 'created_at']


class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'title', 'location', 'price', 'currency', 'created_at', 'is_featured', 'publik_id',
                  'expires_at']


class UserAdListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'title', 'status', 'created_at', 'expires_at']


class FavoriteAdSerializer(serializers.ModelSerializer):
    ad_title = serializers.CharField(source='ad.title', read_only=True)

    class Meta:
        model = FavoriteAd
        fields = ['id', 'ad', 'ad_title', 'created_at']
