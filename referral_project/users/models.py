from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH, REGEX


class User(AbstractUser):
    """Модель пользователя, расширяющая AbstractUser."""

    email = models.EmailField(
        "Почтовый адрес", max_length=MAX_EMAIL_LENGTH, unique=True
    )
    username = models.CharField(
        "Логин",
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        validators=[
            RegexValidator(regex=REGEX, message="Недопустимый символ")
        ],
    )
    first_name = models.CharField("Имя", max_length=MAX_USERNAME_LENGTH)
    last_name = models.CharField("Фамилия", max_length=MAX_USERNAME_LENGTH)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.username
