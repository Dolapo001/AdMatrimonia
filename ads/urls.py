from django.urls import path
from .views import *


urlpatterns = [
    path("category_list/", GetCategoryList.as_view(), name="Category"),
    path("sub_category_list/", GetSubCategoryList.as_view(), name="Sub-Category"),

    path('ads/', ListAdsView.as_view(), name='list-ads'),
    path('ads/create/', CreateAdView.as_view(), name='create-ad'),
    path('ads/<str:id>/', AdDetailView.as_view(), name='ad-detail'),
    path('ads/user/', UserAdsView.as_view(), name='user-ads'),

    path('ads/<str:ad_id>/favorite/', AddToFavoriteView.as_view(), name='add-to-favorite'),
    path('ads/<str:ad_id>/unfavorite/', RemoveFromFavoriteView.as_view(), name='remove-from-favorite'),
    path('ads/favorites/', FavoriteAdsView.as_view(), name='favorite-ads'),

]
