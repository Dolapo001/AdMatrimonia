from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from django.db.models import QuerySet


def paginate_and_filter_queryset(request: Request, queryset: QuerySet, serializer_class, search_fields=None,
                                 ordering_fields=None):
    # Apply filtering
    search_filter = SearchFilter()
    ordering_filter = OrderingFilter()

    if search_fields:
        queryset = search_filter.filter_queryset(request, queryset, None)
    if ordering_fields:
        queryset = ordering_filter.filter_queryset(request, queryset, None)

    # Apply pagination
    paginator = PageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    serialized_data = serializer_class(paginated_queryset, many=True)

    return paginator.get_paginated_response(serialized_data.data)


def get_serializer_error_as_string(errors) -> str:
    error_messages = []
    for field, error_list in errors.items():
        for error in error_list:
            field_label = field.replace("_", " ")
            error_messages.append(f"{field_label} input: {error}")
    return " | ".join(error_messages)
