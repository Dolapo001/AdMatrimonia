from django.urls import path
from .views import *


urlpatterns = [
    path("category_list/", GetCategoryList.as_view(), name="Category"),
    path("sub_category_list/", GetSubCategoryList.as_view(), name="Sub-Category"),

    path('ads/', ListAdsView.as_view(), name='list-ads'),
    path('create/', CreateAdView.as_view(), name='create-ad'),

    path('favorites/', FavoriteAdsView.as_view(), name='favorite-ads'),
    path('<str:ad_id>/favorite/', AddToFavoriteView.as_view(), name='add-to-favorite'),
    path('<str:ad_id>/unfavorite/', RemoveFromFavoriteView.as_view(), name='remove-from-favorite'),
    path('user/', UserAdsView.as_view(), name='user-ads'),

    path('<str:id>/', AdDetailView.as_view(), name='ad-detail'),
]
