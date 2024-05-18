from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    telegram: str
    role: str
    balance: float
