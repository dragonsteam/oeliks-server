from django.contrib.auth.hashers import make_password
from rest_framework.serializers import (
    ModelSerializer,
    # Serializer,
    # SerializerMethodField,
)

from .models import User, Advertisement

# User = get_user_model()

class UserSerializer(ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'password',
            'language',
            'role',
        ]
        # fields = tuple(User.REQUIRED_FIELDS) + (
        #     settings.USER_ID_FIELD,
        #     settings.LOGIN_FIELD,
        # )
        # read_only_fields = (settings.LOGIN_FIELD,)

    def validate_password(self, value: str) -> str:
        """    Hash value passed by user.    :param value: password of a user    :return: a hashed version of the password    """
        return make_password(value)

    # def update(self, instance, validated_data):
    #     email_field = get_user_email_field_name(User)
    #     instance.email_changed = False
    #     if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
    #         instance_email = get_user_email(instance)
    #         if instance_email != validated_data[email_field]:
    #             instance.is_active = False
    #             instance.email_changed = True
    #             instance.save(update_fields=["is_active"])
    #     return super().update(instance, validated_data)



#####################################

class AdvertisementSerializer(ModelSerializer):
    
    class Meta:
        model = Advertisement
        fields = [
            'title',
            'about',
            'price',
            'currency',
            'is_auto_renew',
        ]