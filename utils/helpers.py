import rest_framework
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from json import JSONDecodeError


def custom_response(massage="", data=None, status_code=200):
    return Response(
        {
            "message": massage,
            "data": data,
        },
        status=status_code,
    )
