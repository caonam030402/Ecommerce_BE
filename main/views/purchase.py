from django.views.decorators.csrf import csrf_exempt
from main.services.purchase import PurchaseService
from rest_framework.response import Response
from main.models.purchase import Purchase
from rest_framework import status
from rest_framework import views
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from main.serializers.purchase import PurchaseSerializer
from main.models.promotion import Promotion
from django.http import JsonResponse


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

        return Response(
            data={
                "message": "Thêm vào giỏ hàng thành công",
                "data": serialized_purchase,
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        status = request.GET.get("status")

        if status is None:
            status = 0

        purchase_list = PurchaseService.get_purchases_with_status(
            int(status), request.user.id
        )

        print(purchase_list)

        serializer = PurchaseSerializer(purchase_list, many=True)

        return Response(
            data={
                "message": "Lấy đơn hàng thành công",
                "data": serializer.data,
            },
            status=200,
        )

    @csrf_exempt
    def delete(self, request):
        purchase_ids = request.data.getlist("ids[]")
        deleted_count = Purchase.objects.filter(id__in=purchase_ids).delete()
        return Response(
            f"Xóa {deleted_count} đơn thành công",
            data={"delete_count": deleted_count},
            status=status.HTTP_200_OK,
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

            return Response(
                data={
                    "message": "Mua thành công",
                    "data": serialized_purchase,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

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
        return Response(
            "Cập nhập đơn hàng thành công", data=purchase, status=status.HTTP_200_OK
        )

    # @csrf_exempt
    # def get(self, request, status):
    #     purchases = PurchaseService.get_purchases_with_status(int(status), None)
    #     return Response(
    #         "Lấy đơn mua thành công", data=purchases, status=status.HTTP_200_OK
    #     )
