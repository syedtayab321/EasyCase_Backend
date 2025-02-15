from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework_simplejwt.tokens import RefreshToken

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = sociallogin.user

        if not user.pk:  
            user.save()  # Ensure user is saved before modifying related fields
        
        # ✅ Mark Google-registered users as verified
        if sociallogin.account.provider == "google":
            user.is_verified = True  # If using a custom `is_verified` field
            user.save(update_fields=["is_verified"])  

            # ✅ Mark email as verified in Allauth's EmailAddress model
            user.emailaddress_set.filter(email=user.email).update(verified=True)

        return super().save_user(request, sociallogin, form)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        refresh = RefreshToken.for_user(user)
        return f"/?access_token={str(refresh.access_token)}"
