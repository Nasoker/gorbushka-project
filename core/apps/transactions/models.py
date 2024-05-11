from django.db import models

from core.apps.common.models import TimeStampedModel
from core.apps.users.models import User

from core.apps.transactions.entities.transactions import Transaction as TransactionEntity


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

    # TODO: how to store pdf files in django ????

    comment = models.TextField(
        max_length=2000,  # TODO: 50 is okay?
        blank=True,
        null=True,
        verbose_name='Примечание',
    )

    def to_entity(self) -> TransactionEntity:
        return TransactionEntity(
            id=self.pk,
            transaction_type=self.transaction_type.type,
            client_id=self.client.pk if self.client else None,
            client_username=self.client.username if self.client else None,
            provider=self.provider,
            amount=self.amount,
            comment=self.comment,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'