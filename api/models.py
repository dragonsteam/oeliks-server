from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .validators import UnicodePhoneValidator
from .const import USER_ROLES, LANGUAGES

# models here
class User(AbstractUser):
    phone_validator = UnicodePhoneValidator()
    
    # email = models.EmailField(unique=True)
    # access = models.OneToOneField(Access, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(
        max_length=10,
        unique=True,
        help_text =_(
            "Required. 10 characters. numbers only."
        ),
        validators=[phone_validator],
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    language = models.CharField(max_length=5, null=True, choices=LANGUAGES)
    role = models.CharField(max_length=3, null=True, choices=USER_ROLES)