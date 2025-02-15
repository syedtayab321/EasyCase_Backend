from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # User is verified if email OR phone is verified

    email_otp = models.CharField(max_length=6, blank=True, null=True)
    email_otp_created_at = models.DateTimeField(blank=True, null=True)

    phone_otp = models.CharField(max_length=6, blank=True, null=True)
    phone_otp_created_at = models.DateTimeField(blank=True, null=True)

    def is_otp_valid(self, otp, method="email"):
        """Check if OTP is valid (email or phone)"""
        if method == "email":
            if self.email_otp != otp:
                return False
            expiration_time = self.email_otp_created_at + timedelta(minutes=10)
        elif method == "phone":
            if self.phone_otp != otp:
                return False
            expiration_time = self.phone_otp_created_at + timedelta(minutes=10)
        else:
            return False

        return timezone.localtime(timezone.now()) <= expiration_time
