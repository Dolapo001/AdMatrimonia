from rest_framework import serializers
from .models import Category, SubCategory, Ad


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'display_name', 'icon', 'color', 'is_active', 'order']


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'display_name', 'is_active', 'order', 'category']


class AdSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)

    class Meta:
        model = Ad
        fields = [
            'id', 'title', 'description', 'price', 'currency',
            'location', 'contact_phone', 'contact_email', 'images',
            'status', 'is_featured', 'is_sold', 'is_expired',
            'created_at', 'updated_at', 'expires_at', 'publik_id',
            'category', 'subcategory'
        ]
