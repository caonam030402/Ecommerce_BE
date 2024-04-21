from django.views.decorators.csrf import csrf_exempt
from main.services.purchase import PurchaseService
from rest_framework.response import Response
from main.models.purchase import Purchase
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from main.serializers.purchase import PurchaseSerializer
from django.http import JsonResponse
from utils.helpers import custom_response


class PurchaseAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.user.id

        data = request.data

        product_id = data.get("product_id")
        buy_count = data.get("buy_count")

        purchase = PurchaseService.add_to_cart(product_id, buy_count, user)

        serializer = PurchaseSerializer(purchase)
        serialized_purchase = serializer.data

        return custom_response("Thêm vào giỏ hàng thành công", serialized_purchase, 200)

    def get(self, request):
        status = request.GET.get("status")

        if status is None:
            status = 0

        purchase_list = PurchaseService.get_purchases_with_status(
            int(status), request.user.id
        )

        serializer = PurchaseSerializer(purchase_list, many=True)

        return custom_response("Lấy đơn hàng thành công", serializer.data, 200)

    @csrf_exempt
    def delete(self, request):
        purchase_ids = request.data.getlist("ids[]")
        deleted_count = Purchase.objects.filter(id__in=purchase_ids).delete()
        return custom_response(
            f"Xóa {deleted_count} đơn thành công", {"delete_count": deleted_count}, 200
        )

    def put(self, request):
        try:
            purchase_ids = [
                purchase_data["purchase_id"] for purchase_data in request.data
            ]

            purchases = Purchase.objects.filter(pk__in=purchase_ids)

            for purchase in purchases:
                purchase.status = 1
                purchase.save()

            serializer = PurchaseSerializer(purchase)
            serialized_purchase = serializer.data

            return custom_response("Mua thành công", serialized_purchase, 200)

        except Exception as e:
            return custom_response("error", str(e), 500)

    @csrf_exempt
    def patch(self, request):
        product_id = request.data.get("product_id")
        purchase_id = request.data.get("purchase_id")
        update_body = {
            key: value
            for key, value in request.data.items()
            if key not in ["product_id", "purchase_id"]
        }
        purchase = PurchaseService.update_purchase(product_id, update_body, purchase_id)
        return custom_response("Cập nhật đơn hàng thành công", purchase, 200)
