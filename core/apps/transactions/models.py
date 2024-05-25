import decimal

from django.db import models

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

    customer_balance = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        default=0,
        blank=True,
        null=True,
        verbose_name='Баланс',
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
        max_length=2000,
        blank=True,
        null=True,
        verbose_name='Примечание',
    )

    def save(self, *args, **kwargs):
        if self.customer is not None:
            last_customer_transactions = Transaction.objects.filter(customer=self.customer).order_by('-created_at')[:1]

            if last_customer_transactions:
                self.customer_balance = last_customer_transactions[0].customer_balance + self.amount
            else:
                self.customer_balance = self.amount

            User.objects.filter(id=self.customer.id).update(
                balance=self.customer_balance,
            )

        super().save(*args, **kwargs)

    def to_entity(self) -> TransactionEntity:
        return TransactionEntity(
            id=self.pk,
            transaction_type=self.transaction_type.type,
            transaction_type_id=self.transaction_type.pk,
            customer_id=self.customer.pk if self.customer else None,
            customer_username=self.customer.username if self.customer else None,
            customer_balance=self.customer_balance,
            provider=self.provider,
            amount=self.amount,
            comment=self.comment,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, entity: TransactionEntity) -> 'Transaction':
        return cls(
            pk=entity.id,
            transaction_type=TransactionType.objects.filter(pk=entity.transaction_type_id)[0],
            customer=User.objects.filter(id=entity.customer_id)[0],
            provider=entity.provider,
            amount=decimal.Decimal(entity.amount),
            comment=entity.comment,
        )

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
