from api.validators import username_validator
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
    ROLE_CHOICES = (
        (USER, "Пользователь"),
        (MODERATOR, "Модератор"),
        (ADMIN, "Администратор"),
    )
    username = models.CharField(
        "Имя пользователя",
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        validators=(username_validator,),
    )
    email = models.EmailField(
        "Электронная почта", max_length=settings.LIMIT_EMAIL, unique=True
    )
    role = models.CharField(
        "Роль",
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField("Биография", blank=True)
    first_name = models.CharField(
        "Имя", max_length=settings.LIMIT_USERNAME, blank=True
    )
    last_name = models.CharField(
        "Фамилия", max_length=settings.LIMIT_USERNAME, blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return self.username[: settings.OUTPUT_LENGTH]
