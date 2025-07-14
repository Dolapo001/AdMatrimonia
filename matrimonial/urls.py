from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', GetProfileView.as_view(), name='get_user_profile'),
    path('profile/create/', CreateProfileView.as_view(), name='create_user_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_user_profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_user_profile'),
    path('profiles/', MatrimonyProfileListView.as_view(), name='matrimonia_profiles'),
    path('profiles/<str:user_id>/', MatrimonyProfileDetailView.as_view()),
    path('profile/<str:user_id>/pictures/', MatrimonyProfilePicturesView.as_view()),
    path('profile/pictures/', UploadProfilePictureView.as_view()),
    path('profile/pictures/<str:picture_id>/', DeleteProfilePictureView.as_view()),
]
