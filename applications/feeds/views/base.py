# Rest Framework
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError

# Applications
from feeds.models import Location


class BaseAreaViewSet(GenericViewSet):
    queryset = Location.objects.select_related("entry").all()

    def get_queryset(self):
        ne_lat = self.request.query_params.get("ne_lat")
        ne_lng = self.request.query_params.get("ne_lng")
        sw_lat = self.request.query_params.get("sw_lat")
        sw_lng = self.request.query_params.get("sw_lng")

        if not ne_lat:
            raise ValidationError("Please provide ne_lat in query parameters")
        if not ne_lng:
            raise ValidationError("Please provide ne_lng in query parameters")
        if not sw_lat:
            raise ValidationError("Please provide sw_lat in query parameters")
        if not sw_lng:
            raise ValidationError("Please provide sw_lng in query parameters")
        try:
            ne_lat = float(ne_lat)
            ne_lng = float(ne_lng)
            sw_lat = float(sw_lat)
            sw_lng = float(sw_lng)
        except ValueError:
            raise ValidationError("Please provide float value.")

        return self.queryset.filter(
            northeast_lat__lte=ne_lat,
            northeast_lng__lte=ne_lng,
            southwest_lat__gte=sw_lat,
            southwest_lng__gte=sw_lng,
        )

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        list method retrieves a list of objects in the queryset based on the bounds defined by the
         ne_lat, ne_lng, sw_lat, sw_lng parameters provided in the request query_params.

        The method returns an HTTP 400 BAD REQUEST error if any of the four parameters are not provided in the query.
        If the parameters are not float values, an HTTP error is returned.

        If the input is valid, the method filters the queryset based on the bounds and returns a serialized list of
        objects in the queryset in an HTTP 200 OK response.

        Parameters:
        request (Request): The incoming request object.
        *args: Additional arguments passed to the method.
        **kwargs: Additional keyword arguments passed to the method.

        Returns:
        Response: A serialized list of objects in the queryset within the defined bounds.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(
            data={"count": queryset.count(), "results": serializer.data},
            status=HTTP_200_OK,
        )
