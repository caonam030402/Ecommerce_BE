from rest_framework import views
from rest_framework.response import Response
from main.models.product import Category
from main.serializers.product import CategorySerializer
from main.serializers.product import ProductSerializer
from rest_framework.response import Response
from main.services.product import ProductService
from rest_framework import status
from utils.helpers import custom_response


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
            return custom_response("Get all categories failed!", str(e), 400)

    def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return custom_response(
                    "Create category successfully!", serializer.data, 201
                )
            else:
                return custom_response(
                    "Create category failed!", serializer.errors, 400
                )
        except Exception as e:
            print(e)
            return custom_response("Create category failed!", str(e), 400)


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

                return custom_response(
                    "Lấy sản phẩm thành công",
                    {
                        "products": products_data,
                        "pagination": {
                            "page": paginate.number,
                            "page_size": paginate.paginator.num_pages,
                            "limit": paginate.paginator.per_page,
                        },
                    },
                    200,
                )

            else:
                return custom_response(
                    "Không có sản phẩm nào phù hợp",
                    None,
                    404,
                )
        except Exception as e:
            print(e)
            custom_response("Lỗi", str(e), 500)

    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data, many=True)
            if serializer.is_valid():
                serializer.save()
                return custom_response("Them san pham thanh cong", serializer.data, 201)
            else:
                return custom_response("Them san pham that bai", serializer.errors, 400)

        except Exception as e:
            print(e)
            return custom_response("Them san pham that bai", str(e), 500)


class ProductDetailViewAPI(views.APIView):
    def get(self, request, product_id):
        try:
            product = ProductService.get_product_by_id(product_id)
            if product is not None:
                serializer = ProductSerializer(product)
                return custom_response("Lấy sản phẩm thành công", serializer.data, 200)

            else:
                return custom_response("Không tìm thấy bạn san pham", None, 404)

        except Exception as e:
            print(e)
            return custom_response("Lỗi server", str(e), 500)
