from django.urls import path, include
from .views import VerifyOTPView
from .views import VerifyPhoneOTPView
urlpatterns = [
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path("verify-phone-otp/", VerifyPhoneOTPView.as_view(), name="verify-phone-otp"),
    # path('auth/', include('allauth.urls')),
]
