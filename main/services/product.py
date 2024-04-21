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

            category = request.GET.get("category")
            rating_filter = request.GET.get("rating_filter")
            name = request.GET.get("name", "")
            price_max = request.GET.get("price_max")
            price_min = request.GET.get("price_min")

            products = Product.objects.all()

            if category:
                products = products.filter(category=category)
            if rating_filter:
                products = products.filter(rating__gte=rating_filter)
            if name:
                products = products.filter(name__icontains=name)
            if price_max:
                products = products.filter(price__lte=price_max)
            if price_min:
                products = products.filter(price__gte=price_min)

            if sort_by == "view":
                products = (
                    products.order_by("-view")
                    if order == "desc"
                    else products.order_by("view")
                )
            elif sort_by == "sold":
                products = (
                    products.order_by("-sold")
                    if order == "desc"
                    else products.order_by("sold")
                )
            elif sort_by == "price":
                products = (
                    products.order_by("-price")
                    if order == "desc"
                    else products.order_by("price")
                )
            else:
                products = (
                    products.order_by("-created_at")
                    if order == "desc"
                    else products.order_by("created_at")
                )

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
