from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodePhoneValidator(validators.RegexValidator):
    regex = r"^\d{9}$"
    message = _(
        "Enter a valid phone number. This value may contain only 9 numbers."
    )
    flags = 0


class UnicodeTitleValidator(validators.RegexValidator):
    regex = r".{16,}"
    message = _(
        "Enter a valid text. This value cannot be less than 16 characters."
    )
    flags = 0


def validate_file_size(file):
    max_size_mb = 5
    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f'Files cannot be larger than {max_size_mb}Mb')