from rest_framework.pagination import PageNumberPagination


class LocationPagination(PageNumberPagination):
    """
    Custom pagination for the location API.

    Max page size is set to 100 and can be changed depending on our choice.
    """
    page_size_query_param = "page_size"
    max_page_size = 100
    page_size = 20
