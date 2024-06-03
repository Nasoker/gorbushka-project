from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from core.apps.users.entities.users import User as UserEntity


class User(AbstractUser):
    CUSTOMER = 'Customer'
    CASHIER = 'Cashier'
    MODERATOR = 'Moderator'
    ADMIN = 'Admin'

    ROLE_CHOICES = (
        (CUSTOMER, 'Клиент'),
        (CASHIER, 'Кассир'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
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
        verbose_name='Телеграм',
    )

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
        verbose_name='Роль',
    )

    def __str__(self):
        if not self.last_name:
            return f'{self.first_name} ({self.email})'
        else:
            return f'{self.first_name} {self.last_name} ({self.email})'

    @property
    def is_admin(self) -> bool:
        return self.role == self.ADMIN and self.role == self.is_staff

    @property
    def is_moderator(self) -> bool:
        return self.role == self.MODERATOR and self.role == self.is_staff

    @property
    def is_cashier(self) -> bool:
        return self.role == self.CASHIER

    @property
    def is_customer(self) -> bool:
        return self.role == self.CUSTOMER

    def to_entity(self) -> UserEntity:
        return UserEntity(
            id=self.id,
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=str(self.phone),
            telegram=self.telegram,
            role=self.role,
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
