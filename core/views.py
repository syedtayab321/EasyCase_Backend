from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import VerifyOTPSerializer, CustomUserCreateSerializer
from django.utils.timezone import now
from rest_framework import views

class VerifyOTPView(generics.GenericAPIView):
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class VerifyPhoneOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(phone_number=phone_number)

            # Check OTP and expiration time (5 minutes expiry)
            if user.phone_otp == otp and (now() - user.phone_otp_created_at).seconds < 300:
                user.is_phone_verified = True
                user.phone_otp = None  # Clear OTP
                user.save()
                return Response({"message": "Phone number verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User with this phone number not found"}, status=status.HTTP_404_NOT_FOUND)