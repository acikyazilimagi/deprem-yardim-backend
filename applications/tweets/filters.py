from rest_framework import filters
from rest_framework import serializers

class LocationFilterParamSerializer(serializers.Serializer):
    """
    Filter by query param: created_at
    """
    created_at__gte = serializers.DateTimeField(required=False)
    created_at__lte = serializers.DateTimeField(required=False)



class LocationFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        params = LocationFilterParamSerializer(data=request.query_params)
        params.is_valid(raise_exception=True)
        filters=params.validated_data
        created_at__gte = filters.get("created_at__gte",None)
        created_at__lte = filters.get("created_at__lte",None)
        if created_at__gte:
            queryset = queryset.filter(address__tweet__created_at__gte=created_at__gte)
        if created_at__lte:
            queryset = queryset.filter(address__tweet__created_at__lte=created_at__lte)
        
        return queryset