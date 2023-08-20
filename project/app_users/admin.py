from django.contrib import admin
from app_users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Custom User admin model.
    """

    list_display = (
        'id',
        'username',
        'phone',
        'invite_code',
    )
