from datetime import datetime

from pydantic import BaseModel

from core.apps.transactions.entities.transactions import (
    Transaction as TransactionEntity,
    TransactionType as TransactionTypeEntity,
)


class TransactionInSchema(BaseModel):
    id: int | None = None  # noqa
    transaction_type: str
    customer_id: int | None = None
    provider: str | None = None
    amount: float
    comment: str | None = None

    def to_entity(self):
        return TransactionEntity(
            id=self.id,
            transaction_type=self.transaction_type,
            customer_id=self.customer_id,
            provider=self.provider,
            amount=self.amount,
            comment=self.comment,
            transaction_type_id=None,
            customer_username=None,
            created_at=None,
            updated_at=None,
        )


class TransactionOutSchema(BaseModel):
    id: int
    transaction_type: str
    customer_id: int | None
    customer_username: str | None
    provider: str | None
    amount: float
    comment: str | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: TransactionEntity) -> 'TransactionOutSchema':
        return TransactionOutSchema(
            id=entity.id,
            transaction_type=entity.transaction_type,
            customer_id=entity.customer_id,
            customer_username=entity.customer_username,
            provider=entity.provider,
            amount=entity.amount,
            comment=entity.comment,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class TransactionTypeOutSchema(BaseModel):
    id: int
    type: str

    @staticmethod
    def from_entity(entity: TransactionTypeEntity) -> 'TransactionTypeOutSchema':
        return TransactionTypeOutSchema(
            id=entity.id,
            type=entity.type,
        )
