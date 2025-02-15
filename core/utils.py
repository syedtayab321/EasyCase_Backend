from rest_framework import serializers
from .models import User
import random

from twilio.rest import Client
from django.conf import settings
import random
from django.utils.timezone import now

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_twilio(phone_number, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your verification code is {otp}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return message.sid

def generate_random_otp():
    return str(random.randint(100000, 999999))  # Generates a 6-digit OTP



# {
#     "method": "phone",
#     "value": "+123456789",
#     "otp": "123456"
# }
# {
#     "method": "email",
#     "value": "user@example.com",
#     "otp": "123456"
# }
