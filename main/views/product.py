from rest_framework import views
from rest_framework.response import Response
from main.models.product import Category
from main.serializers.product import CategorySerializer
from utils.helpers import custom_response, parse_request
from main.models.product import Product
from main.serializers.product import ProductSerializer


class CategoryAPIView(views.APIView):
    def get(self, request):
        try:
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(
                {
                    "message": "Get all categories successfully!",
                    "data": serializer.data,
                },
                status=200,
            )
        except Exception as e:
            return Response(
                {
                    "status": 400,
                    "message": "Get all categories failed!",
                    "error": [str(e)],
                },
                status=400,
            )


def post(self, request):
    data = parse_request(request)
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return custom_response(
            "Create category successfully!", "Success", serializer.data, 201
        )
    else:
        return custom_response(
            "Create category failed", "Error", serializer.errors, 400
        )


class ProductViewAPI(views.APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            serializers = ProductSerializer(products, many=True)
            return custom_response(
                "Get all products successfully!", "Success", serializers.data, 200
            )
        except:
            return custom_response("Get all products failed!", "Error", None, 400)
