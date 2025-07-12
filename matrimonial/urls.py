from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', GetProfileView.as_view(), name='get_user_profile'),
    path('profile/create/', CreateProfileView.as_view(), name='create_user_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_user_profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_user_profile'),
]
