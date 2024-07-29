from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from mailings.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    phone = PhoneNumberField(
        verbose_name="Телефон", **NULLABLE, help_text="Введите номер телефона"
    )
    fullname = models.CharField(
        max_length=50,
        verbose_name="Имя пользователя",
        **NULLABLE,
        help_text="Введите ваше имя или ник"
    )
    token = models.CharField(max_length=100, verbose_name="Token", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
