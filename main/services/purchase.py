from django.db.models import F
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from main.models.product import Product
from main.models.purchase import Purchase
from main.serializers.purchase import PurchaseSerializer
from user.models import User


class PurchaseService:

    def add_to_cart(product_id, buy_count, user):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError("Sản phẩm không tồn tại")

        try:
            purchase = Purchase.objects.get(user=user, product=product, status=-1)

            purchase.buy_count += buy_count
            purchase.save()
        except Purchase.DoesNotExist:
            if isinstance(user, int):
                try:
                    user = User.objects.get(id=user)
                except User.DoesNotExist:
                    raise ValueError("User không tồn tại")

            purchase = Purchase.objects.create(
                buy_count=buy_count,
                price=product.price,
                price_before_discount=product.price_before_discount,
                status=-1,
                user=user,
                product=product,
            )
        return purchase

    @staticmethod
    def get_purchases_with_status(status, user_id):
        if status == 0:
            purchases = (
                Purchase.objects.all().select_related("product", "user").order_by("-id")
            )
        else:
            purchases = (
                Purchase.objects.filter(status=status, user_id=user_id)
                .select_related("product", "user")
                .order_by("-id")
            )

        return purchases

    @staticmethod
    def update_purchase(product_id, body_update, purchase_id):
        try:
            if product_id:
                purchases = Purchase.objects.filter(product_id=product_id)
            elif purchase_id:
                purchases = Purchase.objects.filter(id=purchase_id)
            else:
                raise ValueError("Thiếu thông tin cần thiết")

            if purchases.exists():
                purchases.update(**body_update)
                return purchases
            else:
                raise ObjectDoesNotExist("Không tìm thấy bản ghi phù hợp")
        except Exception as e:
            print(f"Error updating purchase: {e}")
            return None
