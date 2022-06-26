import email
from sre_constants import SUCCESS
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" not in username:
                user = UserModel.objects.get(username=username)
            else:
                user = UserModel.objects.get(email=username)
            success = user.check_password(password)
            if(success):
                return user
        except UserModel.DoesNotExist:
            pass
            return None

    def get_user(self, user_id: int):
        try:
            return UserModel.objects.get(pk=user_id)
        except:
            return None        
