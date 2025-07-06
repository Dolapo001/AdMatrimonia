from django.urls import path
from .views import *


urlpatterns = [
    path("category_list/", GetCategoryList.as_view(), name="Category"),
    path("sub_category_list/", GetSubCategoryList.as_view(), name="Sub-Category"),
]
