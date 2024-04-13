from django.utils.deprecation import MiddlewareMixin


class CorsMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set CORS headers
        response["Access-Control-Allow-Origin"] = "http://localhost:4000"
        response["Access-Control-Allow-Methods"] = (
            "DELETE, GET, OPTIONS, PATCH, POST, PUT"
        )
        response["Access-Control-Allow-Headers"] = (
            "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with"
        )

        if request.method == "OPTIONS":
            # Preflight request handling
            response["Access-Control-Max-Age"] = 86400  # 24 hours

        # Set Referrer-Policy header
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
