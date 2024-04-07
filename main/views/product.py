from rest_framework import views
from rest_framework.response import Response
from main.models.product import Category
from main.serializers.product import CategorySerializer
from utils.helpers import custom_response, parse_request
from main.models.product import Product
from main.serializers.product import ProductSerializer
from rest_framework.response import Response
from main.services.product import ProductService
from rest_framework import status


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
            query_params = {
                "page": request.GET.get("page", 1),
                "limit": request.GET.get("limit", 20),
            }

            paginate = ProductService.paginate_and_query_product(request, query_params)
            if paginate is not None:
                serializer = ProductSerializer(paginate.object_list, many=True)
                products_data = serializer.data

                response_data = {
                    "message": "Lấy sản phẩm thành công",
                    "data": {
                        "products": products_data,
                        "pagination": {
                            "page": paginate.number,
                            "page_size": paginate.paginator.num_pages,
                            "limit": paginate.paginator.per_page,
                        },
                    },
                }
                return Response(response_data, status=200)
            else:
                return Response("Không có sản phẩm nào phù hợp", status=404)
        except Exception as e:
            print(e)
            return Response("Lấy thành công", status=500)


class ProductDetailViewAPI(views.APIView):
    def get(self, request, product_id):
        try:
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                serializer = ProductSerializer(product)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    "Không tìm thấy sản phẩm", status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            print(e)
            return Response("Lỗi server", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
