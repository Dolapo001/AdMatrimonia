from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', GetProfileView.as_view(), name='get_user_profile'),
    path('profile/create/', CreateProfileView.as_view(), name='create_user_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_user_profile'),
    path('profile/delete/', DeleteProfileView.as_view(), name='delete_user_profile'),

    path('profiles/', MatrimonyProfileListView.as_view(), name='list_matrimony_profiles'),
    path('profiles/<str:user_id>/', MatrimonyProfileDetailView.as_view(), name='matrimony_profile_detail'),

    path('profile/<str:user_id>/pictures/', MatrimonyProfilePicturesView.as_view(), name='get_profile_pictures'),
    path('profile/pictures/', UploadProfilePictureView.as_view(), name='upload_profile_picture'),
    path('profile/pictures/<str:picture_id>/', DeleteProfilePictureView.as_view(), name='delete_profile_picture'),

    path('preferences/', GetPreferenceView.as_view(), name='get_partner_preferences'),       # GET
    path('preferences/create/', SetPreferenceView.as_view(), name='create_partner_preferences'),  # POST
    path('preferences/update/', UpdatePreferenceView.as_view(), name='update_partner_preferences'),  # PUT
]
