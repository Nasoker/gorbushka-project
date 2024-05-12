from datetime import datetime
from pydantic import BaseModel

from core.apps.transactions.entities.transactions import Transaction as TransactionEntity


class TransactionSchema(BaseModel):
    id: int
    transaction_type: str
    client_id: int | None
    client_username: str | None
    provider: str | None
    amount: float
    comment: str | None
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: TransactionEntity) -> 'TransactionSchema':
        return TransactionSchema(
            id=entity.id,
            transaction_type=entity.transaction_type,
            client_id=entity.client_id,
            client_username=entity.client_username,
            provider=entity.provider,
            amount=entity.amount,
            comment=entity.comment,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
