from collections import OrderedDict
from rest_framework import serializers
from app_users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Custom User Serializer.
    """

    class Meta:
        model = CustomUser
        fields = ('phone',)

    def to_representation(self, instance: CustomUser) -> OrderedDict:
        """
        Method for overwriting `invite_code` and `guests` fields.
        """

        data = super().to_representation(instance)
        data['invite_code'] = instance.invite_code
        data['guests'] = [guest.phone for guest in instance.guests.all()]
        return data


class FindCustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for searching other user.
    """

    class Meta:
        model = CustomUser
        fields = ('invite_code',)

    def to_representation(self, instance: CustomUser) -> OrderedDict:
        """
        Method for overwriting `phone`, `invite_code` and `guests` fields.
        Everything is placed on a `found_profile` key.
        """

        data = OrderedDict()
        data['found_profile'] = {
            'phone': instance.phone,
            'invite_code': instance.invite_code,
            'guests':  [guest.phone for guest in instance.guests.all()],
        }
        return data
