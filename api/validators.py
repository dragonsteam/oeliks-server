from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodePhoneValidator(validators.RegexValidator):
    regex = r"^\d{9}$"
    message = _(
        "Enter a valid phone number. This value may contain only 9 numbers."
    )
    flags = 0