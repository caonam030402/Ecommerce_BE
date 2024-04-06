from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from json import JSONDecodeError


def custom_response(message="", status="Success", data=None, status_code=200):
    response_dict = {
        "message": message,
    }
    if status == "Error":
        response_dict["error"] = data
    else:
        response_dict["data"] = data
        return Response(response_dict, status=status_code)


def parse_request(request):
    try:
        return JSONParser().parse(request)
    except JSONDecodeError:
        return custom_response("JSON decoding error!", "Error", None, 400)


def parse_request(request):
    try:
        return JSONParser().parse(request)
    except JSONDecodeError:
        return custom_response("JSON decoding error!", "Error", None, 400)
