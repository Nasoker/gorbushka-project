from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    phone: str
    telegram: str
    role: str


@dataclass
class Customer(User):
    balance: float


@dataclass
class Employee(User):
    salary: float
