from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_not_forbidden_username
from django.core.validators import RegexValidator, MaxLengthValidator

CHOICES = (
	('user', 'User'),
	('moderator', 'Moderator'),
	('admin', 'Admin'),
)


class CustomUser(AbstractUser):
	username = models.TextField(unique=True, max_length=150,
								validators=[validate_not_forbidden_username, RegexValidator(
									regex=r'^[\w.@+-]+\Z',
									message='Имя пользователя содержит недопустимые символы'),
											MaxLengthValidator(150)])
	email = models.EmailField(
		unique=True,
		max_length=254
	)
	first_name = models.CharField(
		max_length=150,
		blank=True
	)
	last_name = models.CharField(
		max_length=150,
		blank=True
	)
	bio = models.TextField(blank=True)
	role = models.CharField(max_length=10, null=False, default='user', choices=CHOICES)

	class Meta:
		ordering = ('id',)
		verbose_name = 'Пользователь'
		verbose_name_plural = 'пользователи'

	def __str__(self):
		return self.username
