from django.db import models
from django.utils.html import format_html

from core.apps.common.models import TimeStampedModel
from core.apps.transactions.entities.transactions import (
    Transaction as TransactionEntity,
    TransactionType as TransactionTypeEntity,
)
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

    def to_entity(self) -> TransactionTypeEntity:
        return TransactionTypeEntity(
            id=self.pk,
            type=self.type,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, entity: TransactionTypeEntity) -> 'TransactionType':
        return cls(
            id=entity.id,
            type=entity.type,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

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

    customer = models.ForeignKey(
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
        max_digits=12,
        decimal_places=2,
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

    def colored_amount(self):
        color_code = '#77DD77' if self.amount > 0 else '#ff6961'

        return format_html(
            '<span style="color:{0};">{1}</span>',
            color_code,
            self.amount,
        )

    colored_amount.allow_tags = True
    colored_amount.short_description = 'Сумма операции'

    def to_entity(self) -> TransactionEntity:
        return TransactionEntity(
            id=self.pk,
            type=self.transaction_type,
            provider=self.provider,
            amount=float(self.amount),
            comment=self.comment,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, entity: TransactionEntity) -> 'Transaction':
        customer = User.from_entity(entity.customer) if entity.customer else None

        return cls(
            transaction_type=TransactionType.from_entity(entity.type),
            customer=customer,
            amount=float(entity.amount),
            comment=entity.comment,
            provider=entity.provider,
        )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']
