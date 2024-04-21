import hmac
from rest_framework.response import Response
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
import datetime
import urllib.parse
import hashlib
from django.conf import settings
from utils.helpers import custom_response


class PaymentAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def __hmacsha512(self, key, data):
        byteKey = key.encode("utf-8")
        return hmac.new(byteKey, data, hashlib.sha512).hexdigest()

    def post(self, request):
        tmn_code = settings.VNP_TMN_CODE
        hash_secret = settings.VNP_HASH_SECRET
        vnp_url = settings.VNP_URL
        return_url = settings.VNP_RETURN_URL
        print(hash_secret)
        order_id = datetime.datetime.now().strftime("%d%H%M%S")
        amount = request.data.get("amount")
        bank_code = request.data.get("bankCode")

        locale = request.data.get("language", "vn")
        curr_code = "VND"

        vnp_params = {
            "vnp_Version": "2.1.0",
            "vnp_Command": "pay",
            "vnp_TmnCode": tmn_code,
            "vnp_ReturnUrl": return_url,
            "vnp_Locale": locale,
            "vnp_CurrCode": curr_code,
            "vnp_TxnRef": order_id,
            "vnp_OrderInfo": f"Thanh toan cho ma GD: {order_id}",
            "vnp_OrderType": "other",
            "vnp_Amount": amount * 100,
            "vnp_IpAddr": request.META.get("REMOTE_ADDR"),
            "vnp_CreateDate": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
        }

        sign_data = urllib.parse.urlencode(sorted(vnp_params.items()))
        sign_data = sign_data.encode("utf-8")

        if not hash_secret:
            return Response(
                {"error": "Secret key is undefined"}, status=status.HTTP_400_BAD_REQUEST
            )

        signed = self.__hmacsha512(hash_secret, sign_data)

        vnp_params["vnp_SecureHash"] = signed
        vnp_url += "?" + urllib.parse.urlencode(vnp_params)

        return custom_response(
            "Lấy URL thành công!",
            vnp_url,
            200,
        )

    def get(self, request):
        hash_secret = settings.VNP_HASH_SECRET

        vnp_params = dict(request.GET)
        secure_hash = vnp_params.pop("vnp_SecureHash")[0]
        vnp_params.pop("vnp_SecureHashType", None)

        sign_data = urllib.parse.urlencode(sorted(vnp_params.items()))
        sign_data = sign_data.encode("utf-8")

        hmac = hashlib.sha512(hash_secret.encode("utf-8"))
        hmac.update(sign_data)
        signed = hmac.hexdigest()

        if secure_hash == signed:
            return Response(
                {
                    "message": "Thanh toán thành công",
                    "response_code": vnp_params["vnp_ResponseCode"][0],
                }
            )
        else:
            return Response({"message": "Thanh toán thất bại", "response_code": "88"})
