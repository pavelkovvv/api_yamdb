from django.core.exceptions import ValidationError
from django.utils import timezone


def my_year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('%(value) это неправильный год!'),
            params={'value': value},
        )
