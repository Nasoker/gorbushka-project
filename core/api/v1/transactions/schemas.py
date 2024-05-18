from datetime import datetime
from pydantic import BaseModel

from core.apps.transactions.entities.transactions import Transaction as TransactionEntity


class TransactionInSchema(BaseModel):
    id: int | None = None
    transaction_type: str
    client_id: int | None = None
    provider: str | None = None
    amount: float
    comment: str | None = None

    def to_entity(self):
        return TransactionEntity(
            id=self.id,
            transaction_type=self.transaction_type,
            client_id=self.client_id,
            provider=self.provider,
            amount=self.amount,
            comment=self.comment,
            transaction_type_id=None,
            client_balance=None,
            client_username=None,
            created_at=None,
            updated_at=None
        )


class TransactionOutSchema(BaseModel):
    id: int
    transaction_type: str
    client_id: int | None
    client_username: str | None
    client_balance: float | None
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
            client_id=entity.client_id,
            client_username=entity.client_username,
            client_balance=entity.client_balance,
            provider=entity.provider,
            amount=entity.amount,
            comment=entity.comment,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
