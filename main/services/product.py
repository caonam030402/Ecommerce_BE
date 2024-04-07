from django.core.paginator import Paginator
from main.models.product import Product


class ProductService:
    @staticmethod
    def paginate_and_query_product(request, query_params):
        try:
            sort_by = request.GET.get("sort_by", "createdAt")
            order = request.GET.get("order", "asc")
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 20))

            category = query_params.get("category")
            rating_filter = query_params.get("rating_filter")
            name = query_params.get("name", "")
            price_max = query_params.get("price_max")
            price_min = query_params.get("price_min")

            sort_query = {}
            if sort_by in ["view", "sold", "price"]:
                sort_query[sort_by] = 1 if order == "desc" else -1
            # else:
            #     sort_query["createdAt"] = "asc" if order == "asc" else "-asc"

            query = {}
            if category:
                query["category"] = category
            if rating_filter:
                query["rating__gte"] = int(rating_filter)
            if name:
                query["name__icontains"] = name
            if price_max is not None and price_min is not None:
                query["price__range"] = (
                    int(price_min),
                    int(price_max),
                )
            elif price_max is not None:
                query["price__lte"] = int(price_max)
            elif price_min is not None:
                query["price__gte"] = int(price_min)

            products = Product.objects.filter(**query).order_by(**sort_query)

            paginator = Paginator(products, limit)
            paginated_products = paginator.page(page)

            return paginated_products
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_product_by_id(product_id):
        try:
            product = Product.objects.get(id=product_id)
            return product
        except Product.DoesNotExist:
            return None
