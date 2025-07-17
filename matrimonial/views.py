from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from common.response_managers import *
import logging

logger = logging.getLogger(__name__)


class GetProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def get(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if not profile:
                return ResponseManager.not_found_response(ResponseStatus.PROFILE_NOT_FOUND)

            serializer = self.serializer_class(profile)
            return ResponseManager.success_response(
                message=ResponseStatus.PROFILE_FETCHED,
                data=serializer.data
            )

        except Exception as e:
            return ResponseManager.handle_exception(e, "fetching user profile")


class CreateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return ResponseManager.created_response(
                    message=ResponseStatus.PROFILE_CREATED,
                    data=serializer.data
                )
            return ResponseManager.validation_error_response(
                errors=serializer.errors
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "creating user profile")


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def put(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if not profile:
                return ResponseManager.not_found_response(ResponseStatus.PROFILE_NOT_FOUND)

            serializer = self.serializer_class(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return ResponseManager.success_response(
                    message=ResponseStatus.PROFILE_UPDATED,
                    data=serializer.data
                )
            return ResponseManager.validation_error_response(
                errors=serializer.errors
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "updating user profile")


class DeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if not profile:
                return ResponseManager.not_found_response(ResponseStatus.PROFILE_NOT_FOUND)

            profile.delete()
            return ResponseManager.deleted_response(ResponseStatus.PROFILE_DELETED)
        except Exception as e:
            return ResponseManager.handle_exception(e, "deleting user profile")


class MatrimonyProfileListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfileSerializer

    def get(self, request):
        try:
            filters = request.query_params
            queryset = MatrimonyProfile.objects.list_profiles(filters)

            return ResponseManager.paginated_response(
                queryset=queryset,
                request=request,
                serializer_class=self.serializer_class,
                message=ResponseStatus.PROFILES_FETCHED,
                page_size=10
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "listing profiles")


class MatrimonyProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(user_id)
            if not profile:
                return ResponseManager.not_found_response(ResponseStatus.PROFILE_NOT_FOUND)

            serializer = MatrimonyProfileSerializer(profile)
            return ResponseManager.success_response(
                message=ResponseStatus.PROFILE_FETCHED,
                data=serializer.data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "fetching profile details")


class MatrimonyProfilePicturesView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfilePictureSerializer

    def get(self, request, user_id):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(user_id)
            if not profile:
                return ResponseManager.not_found_response(ResponseStatus.PROFILE_NOT_FOUND)

            pictures = profile.pictures.all()
            serializer = self.serializer_class(pictures, many=True)
            return ResponseManager.success_response(
                message=ResponseStatus.PICTURES_FETCHED,
                data=serializer.data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "fetching profile pictures")


class UploadProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MatrimonyProfilePictureSerializer

    def post(self, request):
        try:
            profile = MatrimonyProfile.objects.get_by_user_id(request.user.id)
            if not profile:
                return ResponseManager.not_found_response(ResponseStatus.PROFILE_NOT_FOUND)

            image = request.FILES.get('image')
            if not image:
                return ResponseManager.validation_error_response(
                    message=ResponseStatus.IMAGE_REQUIRED
                )

            picture = profile.pictures.create(image=image)
            serializer = self.serializer_class(picture)
            return ResponseManager.created_response(
                message=ResponseStatus.PICTURE_UPLOADED,
                data=serializer.data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "uploading profile picture")


class DeleteProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, picture_id):
        try:
            picture = MatrimonyProfilePicture.objects.filter(
                id=picture_id,
                profile__user=request.user
            ).first()

            if not picture:
                return ResponseManager.not_found_response(ResponseStatus.PICTURE_NOT_FOUND)

            picture.delete()
            return ResponseManager.deleted_response(ResponseStatus.PICTURE_DELETED)
        except Exception as e:
            return ResponseManager.handle_exception(e, "deleting profile picture")


class GetPreferenceView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerPreferenceSerializer

    def get(self, request):
        try:
            preference = PartnerPreference.objects.get_for_user(request.user)
            if not preference:
                return ResponseManager.not_found_response(ResponseStatus.PREFERENCES_NOT_SET)

            serializer = self.serializer_class(preference)
            return ResponseManager.success_response(
                message=ResponseStatus.PREFERENCES_FETCHED,
                data=serializer.data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "fetching partner preferences")


class SetPreferenceView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerPreferenceSerializer

    def post(self, request):
        try:
            if PartnerPreference.objects.get_for_user(request.user):
                return ResponseManager.validation_error_response(
                    message=ResponseStatus.PREFERENCES_EXIST
                )

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return ResponseManager.created_response(
                    message=ResponseStatus.PREFERENCES_CREATED,
                    data=serializer.data
                )
            return ResponseManager.validation_error_response(
                errors=serializer.errors
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "creating partner preferences")


class UpdatePreferenceView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PartnerPreferenceSerializer

    def put(self, request):
        try:
            preference = PartnerPreference.objects.get_for_user(request.user)
            if not preference:
                return ResponseManager.not_found_response(ResponseStatus.PREFERENCES_NOT_FOUND)

            serializer = self.serializer_class(preference, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return ResponseManager.success_response(
                    message=ResponseStatus.PREFERENCES_UPDATED,
                    data=serializer.data
                )
            return ResponseManager.validation_error_response(
                errors=serializer.errors
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "updating partner preferences")


class SendConnectionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendConnectionRequestSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return ResponseManager.validation_error_response(
                    errors=serializer.errors
                )

            receiver_id = serializer.validated_data['receiver_id']
            message = serializer.validated_data.get('message', '')

            receiver = User.objects.filter(id=receiver_id).first()
            if not receiver:
                return ResponseManager.not_found_response(ResponseStatus.USER_NOT_FOUND)

            try:
                connection, created = ConnectionRequest.objects.send(
                    request.user, receiver, message
                )
                status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
                return ResponseManager.success_response(
                    message=ResponseStatus.CONNECTION_SENT,
                    data=ConnectionRequestSerializer(connection).data,
                    status_code=status_code
                )
            except ValueError as e:
                return ResponseManager.validation_error_response(
                    message=str(e)
                )
        except Exception as e:
            return ResponseManager.handle_exception(e, "sending connection request")


class ReceivedConnectionView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestSerializer

    def get(self, request):
        try:
            connections = ConnectionRequest.objects.get_received(request.user)
            if not connections:
                return ResponseManager.not_found_response(ResponseStatus.NO_RECEIVED_CONNECTIONS)

            serializer = self.serializer_class(connections, many=True)
            return ResponseManager.success_response(
                message=ResponseStatus.CONNECTIONS_FETCHED,
                data=serializer.data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "fetching received connections")


class SentConnectionViews(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConnectionRequestSerializer

    def get(self, request):
        try:
            connections = ConnectionRequest.objects.get_sent(request.user)
            if not connections:
                return ResponseManager.not_found_response(ResponseStatus.NO_SENT_CONNECTIONS)

            serializer = self.serializer_class(connections, many=True)
            return ResponseManager.success_response(
                message=ResponseStatus.CONNECTIONS_FETCHED,
                data=serializer.data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "fetching sent connections")


class RespondConnectionsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RespondConnectionRequestSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return ResponseManager.validation_error_response(
                    errors=serializer.errors
                )

            sender_id = serializer.validated_data['sender_id']
            status_value = serializer.validated_data['status']

            sender = User.objects.filter(id=sender_id).first()
            if not sender:
                return ResponseManager.not_found_response(ResponseStatus.USER_NOT_FOUND)

            connection = ConnectionRequest.objects.respond(sender, request.user, status_value)
            if not connection:
                return ResponseManager.not_found_response(ResponseStatus.CONNECTION_NOT_FOUND)

            return ResponseManager.success_response(
                message=ResponseStatus.CONNECTION_RESPONDED,
                data=ConnectionRequestSerializer(connection).data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "responding to connection request")


class BookmarkToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            profile_id = request.data.get('profile_id')
            if not profile_id:
                return ResponseManager.validation_error_response(
                    message="Profile ID is required"
                )

            try:
                profile = MatrimonyProfile.objects.get(id=profile_id)
            except MatrimonyProfile.DoesNotExist:
                return ResponseManager.not_found_response(ResponseStatus.PROFILE_NOT_FOUND)

            bookmarked = Bookmark.objects.toggle(request.user, profile)
            return ResponseManager.success_response(
                message=ResponseStatus.BOOKMARK_TOGGLED,
                data={"bookmarked": bookmarked}
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "toggling bookmark")


class BookmarkListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer

    def get(self, request):
        try:
            bookmarks = Bookmark.objects.get_user_bookmarks(request.user)
            if not bookmarks:
                return ResponseManager.not_found_response(ResponseStatus.BOOKMARK_LIST_NOT_FOUND)

            serializer = self.serializer_class(bookmarks, many=True)
            return ResponseManager.success_response(
                message=ResponseStatus.BOOKMARKS_FETCHED,
                data=serializer.data
            )
        except Exception as e:
            return ResponseManager.handle_exception(e, "fetching bookmarks")

