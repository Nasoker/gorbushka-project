from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    id: int | None
    transaction_type: str
    transaction_type_id: int | None
    customer_id: int | None
    customer_username: str | None
    provider: str | None
    amount: float
    comment: str | None
    created_at: datetime | None
    updated_at: datetime | None


@dataclass
class TransactionType:
    id: int
    type: str
    created_at: datetime
    updated_at: datetime
