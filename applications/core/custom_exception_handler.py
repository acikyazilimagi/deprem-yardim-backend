from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    If the error is handled, return the response, else return a generic error message

    :param exc: The exception instance raised
    :param context: The exception handler gets passed the full Django view arguments
    :return: A response object with a string message field
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Handle DRF errors
    if response is not None:
        response = Response(
            {"message": response.data[0]}, status=status.HTTP_400_BAD_REQUEST
        )

    # Handle custom errors (We don't have any yet)

    # Return 500 Error if no error is handled
    if response is None:
        response = Response(
            {"message": "Something went wrong"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
