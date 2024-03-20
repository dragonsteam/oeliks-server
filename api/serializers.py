from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

# from django_telegram_login.authentication import verify_telegram_authentication
# from django_telegram_login.errors import NotTelegramDataError, TelegramDataIsOutdatedError 
from .auth import verify_telegram_authentication, NotTelegramDataError, TelegramDataIsOutdatedError
from .models import User, Advertisement, AdImage, Section, Category

from core.utility import log
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
    auth_date = serializers.IntegerField()
    username = serializers.CharField()
    photo_url = serializers.CharField()

    class Meta:
        model = User
        fields = ['id', 'hash', 'auth_date', 'username', 'photo_url', 'first_name', 'last_name']

    def to_internal_value(self, data):

        data = super().to_internal_value(data)
        # check authorization
        try:
            check_result = verify_telegram_authentication(settings.TELEGRAM_BOT_TOKEN, request_data=data)
            log(check_result)
        except TelegramDataIsOutdatedError:
            raise serializers.ValidationError({"name": "hash is outdated"})
        except NotTelegramDataError:
            raise serializers.ValidationError({"name": "hash is invalid"})

        return data

    def create(self, validated_data):
        tg_id = validated_data.pop('id')
        tg_hash = validated_data.pop('hash')
        auth_date = validated_data.pop('auth_date')
        photo_url = validated_data.pop('photo_url')
        try:
            return User.objects.get(tg_id=tg_id)
        except User.DoesNotExist:
            return User.objects.create(tg_id=tg_id, **validated_data)


#####################################


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class SectionSerializer(serializers.ModelSerializer):
    section_category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'name', 'section_category')


#####################################
        

class AdImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImage
        fields = ['id', 'image']


class AdvertisementSerializer(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()
    # pictures = AdImageSerializer(many=True, read_only=True)

    class Meta:
        model = Advertisement
        fields = [
            'id',
            'title',
            'description',
            'price',
            'currency',
            'date_posted',
            'pictures',
        ]
        read_only_fields = ['date_posted']

    def get_pictures(self, obj):
        pics = obj.ad_images.all()
        pics_serializer = AdImageSerializer(pics, many=True)
        return pics_serializer.data
    
    def to_internal_value(self, data):
        pictures_value = data.get('pictures', [])
        validated_pictures_value = self.validate_pictures(pictures_value)
        # data['pictures'] = validated_pictures_value
        self.context['pictures'] = validated_pictures_value
        return super().to_internal_value(data)

    def validate_pictures(self, value):
        # if not value:
        #     raise serializers.ValidationError("pictures must container at leaste 1 value")
        return value
    
    def create(self, validated_data):
        user = self.context.get('user')
        new_ad = Advertisement.objects.create(user=user, **validated_data)
        # point selected pictures to this ad
        AdImage.objects.filter(id__in=self.context.get('pictures', []), ad__isnull=True).update(ad=new_ad)
        return new_ad