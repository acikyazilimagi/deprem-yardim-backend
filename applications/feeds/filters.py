from rest_framework import filters
from rest_framework import serializers

class TimestampFilterParamSerializer(serializers.Serializer):
    """
    Filter by query param: timestamp
    """
    timestamp__gte = serializers.DateTimeField(required=False)
    timestamp__lte = serializers.DateTimeField(required=False)



class TimestampFilterBackend(filters.BaseFilterBackend):
    """
    Filter for timestamp filter.
    """
    def filter_queryset(self, request, queryset, view):
        params = TimestampFilterParamSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        filters=params.validated_data
        timestamp__gte = filters.get("raw__timestamp__gte",None)
        timestamp__lte = filters.get("raw__timestamp__lte",None)
        if timestamp__gte:
            queryset = queryset.filter(raw__timestamp__gte=timestamp__gte)
        if timestamp__lte:
            queryset = queryset.filter(raw__timestamp__lte=timestamp__lte)

        return queryset