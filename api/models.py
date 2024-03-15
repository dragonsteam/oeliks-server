from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from django.utils.translation import gettext_lazy as _

from .validators import UnicodePhoneValidator, UnicodeTitleValidator, validate_file_size
from .const import USER_ROLES, LANGUAGES, CURRENCIES

# models here
class User(AbstractBaseUser):
    phone_validator = UnicodePhoneValidator()
    
    # email = models.EmailField(unique=True)
    # access = models.OneToOneField(Access, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        blank=True
    )
    phone = models.CharField(
        max_length=9,
        unique=True,
        help_text =_(
            "Required. 9 characters. numbers only."
        ),
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    language = models.CharField(max_length=5, null=True, choices=LANGUAGES)
    role = models.CharField(max_length=3, null=True, choices=USER_ROLES)

    tg_id = models.BigIntegerField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"


class Section(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='section_category')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)


class Advertisement(models.Model):
    title_validator = UnicodeTitleValidator()

    title = models.CharField(
        max_length=70,
        validators=[title_validator],
    )
    # category
    description = models.CharField(max_length=2048, blank=True)
    exchange_method = models.CharField(max_length=1, choices=[('p', 'priced'), ('e', 'exchange'), ('f', 'free')])
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCIES)
    is_auto_renew = models.BooleanField(default=False) # repost the Ad when expires
    # address = 
    # phone_number
    # email_address
    date_posted = models.DateTimeField(_("date posted"), default=timezone.now)
    is_active = models.BooleanField(default=True)


class AdImage(models.Model):
    ad = models.ForeignKey(Advertisement, null=True, on_delete=models.SET_NULL, related_name='ad_images')
    image = models.ImageField(upload_to='ad/images', validators=[validate_file_size])