from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    CUSTOMER = 'Customer'
    CASHIER = 'Cashier'
    MODERATOR = 'Moderator'
    ADMIN = 'Admin'

    ROLE_CHOICES = (
        (CUSTOMER, 'Customer'),
        (CASHIER, 'Cashier'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Admin')
    )

    phone = PhoneNumberField(
        region='RU',
        unique=True,
        verbose_name='Номер телефона',
    )

    telegram = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name='Телеграм'
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
        verbose_name='Роль'
    )

    def __str__(self):
        if not self.last_name:
            return f'{self.first_name} ({self.email})'
        else:
            return f'{self.first_name} {self.last_name} ({self.email})'

    @property
    def is_admin(self):
        return self.role == self.ADMIN and self.role == self.is_staff

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR and self.role == self.is_staff

    @property
    def is_cashier(self):
        return self.role == self.CASHIER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
