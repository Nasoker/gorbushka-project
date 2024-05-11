from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transaction:
    id: int
    transaction_type: str
    client_id: int
    client_username: str
    provider: str
    amount: float
    comment: str
    created_at: datetime
    updated_at: datetime
