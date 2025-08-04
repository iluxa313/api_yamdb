from django.core.exceptions import ValidationError


def validate_not_forbidden_username(value):
    forbidden_usernames = ['me']
    if value in forbidden_usernames:
        raise ValidationError(
            f'Имя пользователя "{value}" запрещено.',
            params={'value': value},
        )
