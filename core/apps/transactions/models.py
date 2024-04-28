from django.db import models
from core.apps.common.models import TimeStampedModel
from core.apps.users.models import User


class TransactionType(TimeStampedModel):
    type = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Название',
    )

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип транзакции'
        verbose_name_plural = 'Типы транзакций'


class Transaction(TimeStampedModel):
    transaction_type = models.ForeignKey(
        TransactionType,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name='Тип транзакции',
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Клиент',
        limit_choices_to={'role': 'Customer'},
    )

    provider = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Поставщик',
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        blank=False,
        null=False,
        verbose_name='Сумма операции',
    )

    comment = models.TextField(
        max_length=2000,
        blank=True,
        null=True,
        verbose_name='Примечание',
    )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
