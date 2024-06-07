from datetime import datetime

from pydantic import BaseModel

from core.apps.transactions.entities.transactions import (
    Transaction as TransactionEntity,
    TransactionType as TransactionTypeEntity,
)


class TransactionOutSchema(BaseModel):
    id: int
    transaction_type: str
    provider: str | None
    amount: float
    comment: str | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: TransactionEntity) -> 'TransactionOutSchema':
        return TransactionOutSchema(
            id=entity.id,
            transaction_type=entity.type.type,
            provider=entity.provider,
            amount=entity.amount,
            comment=entity.comment,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )


class TransactionsTotalOutSchema(BaseModel):
    total: float


class TransactionTypeOutSchema(BaseModel):
    id: int
    type: str

    @staticmethod
    def from_entity(entity: TransactionTypeEntity) -> 'TransactionTypeOutSchema':
        return TransactionTypeOutSchema(
            id=entity.id,
            type=entity.type,
        )
