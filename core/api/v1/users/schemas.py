from pydantic import BaseModel

from core.apps.users.models import User as UserEntity


class UserOutSchema(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    telegram: str | None = None
    role: str
    balance: float | None = None

    @staticmethod
    def from_entity(entity: UserEntity) -> 'UserOutSchema':
        return UserOutSchema(
            id=entity.id,
            username=entity.username,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            phone=entity.phone,
            telegram=entity.telegram,
            role=entity.role,
            balance=entity.balance,
        )


class UserBalanceOutSchema(BaseModel):
    id: int
    balance: float
