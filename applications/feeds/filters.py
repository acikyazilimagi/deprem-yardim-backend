# Rest Framework
from rest_framework import filters

# Applications
from feeds.serializers import LocationFilterParamSerializer


class LocationFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        params = LocationFilterParamSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        filter_list = params.validated_data
        timestamp__gte = filter_list.get("raw__timestamp__gte", None)
        timestamp__lte = filter_list.get("raw__timestamp__lte", None)
        if timestamp__gte:
            queryset = queryset.filter(raw__timestamp__gte=timestamp__gte)
        if timestamp__lte:
            queryset = queryset.filter(raw__timestamp__lte=timestamp__lte)

        return queryset
