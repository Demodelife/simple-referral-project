from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from app_users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Inherited from `AbstractBaseUser`, CustomUser model.
    Replaces default `User` model.
    """

    username = models.CharField(_('username'), max_length=150, unique=True)
    phone = models.CharField(_('phone number'), max_length=16, null=False, blank=False, unique=True)
    invite_code = models.CharField(_('invite code'), max_length=6, null=False, blank=True)
    guests = models.ManyToManyField('self', symmetrical=False, blank=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
