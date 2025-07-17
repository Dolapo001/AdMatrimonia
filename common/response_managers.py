from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
import logging

logger = logging.getLogger(__name__)


class ResponseManager:
    """
    Centralized response manager for consistent API responses
    """

    @staticmethod
    def success_response(message="Success", data=None, status_code=status.HTTP_200_OK):
        """
        Standard success response format
        """
        response_data = {
            "status": True,
            "message": message
        }
        if data is not None:
            response_data["data"] = data

        return Response(response_data, status=status_code)

    @staticmethod
    def error_response(message="An error occurred", error=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Standard error response format
        """
        response_data = {
            "status": False,
            "message": message
        }
        if error is not None:
            response_data["error"] = str(error)

        return Response(response_data, status=status_code)

    @staticmethod
    def validation_error_response(message="Validation failed", errors=None):
        """
        Standard validation error response format
        """
        response_data = {
            "status": False,
            "message": message
        }
        if errors is not None:
            response_data["errors"] = errors

        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def not_found_response(message="Resource not found"):
        """
        Standard 404 response format
        """
        return Response({
            "status": False,
            "message": message
        }, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def created_response(message="Resource created successfully", data=None):
        """
        Standard 201 response format
        """
        response_data = {
            "status": True,
            "message": message
        }
        if data is not None:
            response_data["data"] = data

        return Response(response_data, status=status.HTTP_201_CREATED)

    @staticmethod
    def deleted_response(message="Resource deleted successfully"):
        """
        Standard 204 response format
        """
        return Response({
            "status": True,
            "message": message
        }, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def unauthorized_response(message="Unauthorized access"):
        """
        Standard 401 response format
        """
        return Response({
            "status": False,
            "message": message
        }, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def forbidden_response(message="Access forbidden"):
        """
        Standard 403 response format
        """
        return Response({
            "status": False,
            "message": message
        }, status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def server_error_response(message="Internal server error", error=None):
        """
        Standard 500 response format
        """
        response_data = {
            "status": False,
            "message": message
        }
        if error is not None:
            response_data["error"] = str(error)

        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def paginated_response(queryset, request, serializer_class, message="Data fetched successfully", page_size=10):
        """
        Standard paginated response format
        """
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = serializer_class(result_page, many=True)

        return paginator.get_paginated_response({
            "status": True,
            "message": message,
            "data": serializer.data
        })

    @staticmethod
    def custom_paginated_response(request, queryset, serializer_class, search_fields=None, ordering_fields=None,
                                  message="Data fetched successfully"):
        """
        Custom paginated response that works with the paginate_and_filter_queryset utility
        This method should be used when you need to maintain compatibility with existing utilities
        """
        try:
            # Import here to avoid circular imports
            from common.utils import paginate_and_filter_queryset

            return paginate_and_filter_queryset(
                request,
                queryset,
                serializer_class,
                search_fields=search_fields or [],
                ordering_fields=ordering_fields or []
            )
        except Exception as e:
            return ResponseManager.server_error_response(
                message=f"An error occurred while {message.lower()}",
                error=str(e)
            )

    @staticmethod
    def handle_exception(exception, context="operation", log_error=True):
        """
        Standard exception handler with logging
        """
        if log_error:
            logger.error(f"Error in {context}: {exception}")

        return ResponseManager.server_error_response(
            message=f"An error occurred during {context}",
            error=str(exception)
        )


class ResponseStatus:
    """
    Constants for response status codes and messages
    """

    # Success messages
    PROFILE_CREATED = "Profile created successfully"
    PROFILE_UPDATED = "Profile updated successfully"
    PROFILE_DELETED = "Profile deleted successfully"
    PROFILE_FETCHED = "Profile fetched successfully"
    PROFILES_FETCHED = "Profiles fetched successfully"

    PICTURE_UPLOADED = "Picture uploaded successfully"
    PICTURE_DELETED = "Picture deleted successfully"
    PICTURES_FETCHED = "Pictures fetched successfully"

    PREFERENCES_CREATED = "Partner preferences created successfully"
    PREFERENCES_UPDATED = "Partner preferences updated successfully"
    PREFERENCES_FETCHED = "Partner preferences fetched successfully"

    CONNECTION_SENT = "Connection request sent successfully"
    CONNECTION_RESPONDED = "Connection request responded successfully"
    CONNECTIONS_FETCHED = "Connections fetched successfully"

    BOOKMARK_TOGGLED = "Bookmark toggled successfully"
    BOOKMARKS_FETCHED = "Bookmarks fetched successfully"

    # Ads related messages
    AD_CREATED = "Ad created successfully"
    AD_UPDATED = "Ad updated successfully"
    AD_DELETED = "Ad deleted successfully"
    AD_FETCHED = "Ad fetched successfully"
    ADS_FETCHED = "Ads fetched successfully"

    CATEGORIES_FETCHED = "Categories fetched successfully"
    SUBCATEGORIES_FETCHED = "Subcategories fetched successfully"

    USER_ADS_FETCHED = "User ads fetched successfully"
    FAVORITE_ADS_FETCHED = "Favorite ads fetched successfully"

    AD_ADDED_TO_FAVORITES = "Ad added to favorites"
    AD_REMOVED_FROM_FAVORITES = "Ad removed from favorites"
    AD_ALREADY_IN_FAVORITES = "Ad already in favorites"

    SEARCH_HISTORY_FETCHED = "Search history fetched successfully"

    # Error messages
    PROFILE_NOT_FOUND = "Profile not found"
    USER_NOT_FOUND = "User not found"
    PICTURE_NOT_FOUND = "Picture not found"
    PREFERENCES_NOT_FOUND = "Partner preferences not found"
    CONNECTION_NOT_FOUND = "Connection request not found"
    BOOKMARK_NOT_FOUND = "Bookmark not found"

    AD_NOT_FOUND = "Ad not found or is no longer active"
    FAVORITE_NOT_FOUND = "Favorite not found"

    IMAGE_REQUIRED = "Image is required"
    UNAUTHORIZED_ACCESS = "Unauthorized access"
    VALIDATION_FAILED = "Validation failed"
    PREFERENCES_EXIST = "Preferences already exist. Use update instead"
    PREFERENCES_NOT_SET = "Partner preferences not set yet"
    NO_RECEIVED_CONNECTIONS = "No received connections"
    NO_SENT_CONNECTIONS = "No sent connections"
    BOOKMARK_LIST_NOT_FOUND = "Bookmark list not found"