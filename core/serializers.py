from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.core.mail import send_mail
from django.conf import settings
from .models import User
from .utils import generate_random_otp
from django.utils import timezone
from .utils import generate_otp, send_otp_via_twilio
from rest_framework import serializers
from django.utils.timezone import now


class UserCreateSerializer(BaseUserCreateSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone_number', 'first_name', 'last_name']

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone_number'):
            raise serializers.ValidationError("Either email or phone number is required.")
        return attrs

    def create(self, validated_data):
        user = super().create(validated_data)
        user.is_active = False  # User is inactive until verification
        user.save()

        if user.email:
            # Generate and send email OTP
            email_otp = generate_otp()
            user.email_otp = email_otp
            user.email_otp_created_at = now()
            user.save()

            send_mail(
                'Verify Your Email',
                f'Your OTP for email verification is: {email_otp}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

        if user.phone_number:
            # Generate and send phone OTP
            phone_otp = generate_otp()
            user.phone_otp = phone_otp
            user.phone_otp_created_at = now()
            user.save()

            send_otp_via_twilio(user.phone_number, phone_otp)

        return user



class VerifyOTPSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=["email", "phone"])  # Select verification method
    value = serializers.CharField()  # Email or Phone Number
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        method = data["method"]
        value = data["value"]
        otp = data["otp"]

        if method == "email":
            user = User.objects.filter(email=value).first()
            if not user:
                raise serializers.ValidationError("User with this email does not exist.")
            if not user.is_otp_valid(otp, method="email"):
                raise serializers.ValidationError("Invalid or expired OTP.")
            user.is_email_verified = True  # Mark email as verified
            user.email_otp = None
            user.email_otp_created_at = None

        elif method == "phone":
            user = User.objects.filter(phone_number=value).first()
            if not user:
                raise serializers.ValidationError("User with this phone number does not exist.")
            if not user.is_otp_valid(otp, method="phone"):
                raise serializers.ValidationError("Invalid or expired OTP.")
            user.is_phone_verified = True  # Mark phone as verified
            user.phone_otp = None
            user.phone_otp_created_at = None

        user.is_verified = user.is_email_verified or user.is_phone_verified
        user.is_active = user.is_verified  # Activate user if verified
        user.save()

        return {"message": "OTP verified successfully!"}

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'password', 'phone_number')

    def create(self, validated_data):
        user = super().create(validated_data)

        # Generate and send OTP if phone number is provided
        if user.phone_number:
            otp = generate_otp()
            user.phone_otp = otp
            user.phone_otp_created_at = now()
            user.save()
            send_otp_via_twilio(user.phone_number, otp)

        return user