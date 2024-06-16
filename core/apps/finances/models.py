from django.db import models

from core.apps.common.models import TimeStampedModel
from core.apps.finances.entities.finances import Finances as FinancesEntity


class Finances(TimeStampedModel):
    """Used to store other finance data.

    Only one record should exist at a time

    """

    amount_in_goods = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        blank=False,
        null=False,
        verbose_name='Сумма в товаре',
    )

    amount_in_defects = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        blank=False,
        null=False,
        verbose_name='Сумма в браке',
    )

    def to_entity(self) -> FinancesEntity:
        return FinancesEntity(
            id=self.pk,
            amount_in_goods=float(self.amount_in_goods),
            amount_in_defects=float(self.amount_in_defects),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_entity(cls, entity: FinancesEntity) -> 'Finances':
        return cls(
            amount_in_goods=entity.amount_in_goods,
            amount_in_defects=entity.amount_in_defects,
        )

    class Meta:
        verbose_name = 'Финансы'
        verbose_name_plural = 'Финансы'
