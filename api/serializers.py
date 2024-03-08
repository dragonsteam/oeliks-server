import logging
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User, Advertisement, AdImage

# User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
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

class TelegramUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    hash = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'hash', 'first_name', 'last_name']

    def create(self, validated_data):
        tg_id = validated_data.pop('id')
        tg_hash = validated_data.pop('hash')
        try:
            return User.objects.get(tg_id=tg_id)
        except User.DoesNotExist:
            new_user = User.objects.create(tg_id=tg_id, **validated_data)

        # logging.warn("shit data", self)
        return User.objects.all()[0]
    
    def check_hash():
        return True

#####################################


class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'ad', 'image']

    # def create(self, validated_data):
    #     ad_id = self.context['ad_id', None]
    #     return AdImage.objects.create(ad_id=ad_id, **validated_data)


class AdvertisementSerializer(serializers.ModelSerializer):
    # image = AdImageSerializer()
    class Meta:
        model = Advertisement
        fields = [
            # 'image',
            'title',
            'about',
            'price',
            'currency',
            'date_posted',
        ]