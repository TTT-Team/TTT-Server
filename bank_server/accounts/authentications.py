from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        phone = kwargs.get('phone')
        if phone:
            try:
                user = User.objects.get(phone=phone)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        return super().authenticate(request, username, password, **kwargs)