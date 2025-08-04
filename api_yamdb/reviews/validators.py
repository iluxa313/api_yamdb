import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value > int(timezone.now().year):
        raise ValidationError(
            f'Год выпуска не может быть больше текущего.',
            params={'value': value},
        )


def validate_slug(value):
    if not re.match(r'^[-a-zA-Z0-9_]+$', value):
        raise ValidationError(
            'Slug может содержать только латинские буквы, цифры, дефисы и подчеркивания.',
            params={'value': value},
        )
    return value
