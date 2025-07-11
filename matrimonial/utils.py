def apply_profile_filters(queryset, params):
    if params.get('gender'):
        queryset = queryset.filter(gender=params['gender'])
    if params.get('religion'):
        queryset = queryset.filter(religion__icontains=params['religion'])
    return queryset
