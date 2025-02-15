from django.contrib.auth.backends import ModelBackend
from core.models import User  # Import your User model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if not user.is_verified:  # Check if OTP is verified
                return None  # Block login if not verified
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
