from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from app_users.models import CustomUser


class CustomAuthBackend(BaseBackend):
    """
    Custom authenticate backend.
    """

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            user = CustomUser.objects.get(
                Q(username=username) | Q(phone=username)
            )

        except CustomUser.DoesNotExist:
            return None

        return user
