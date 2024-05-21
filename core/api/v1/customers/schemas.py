from pydantic import BaseModel

from core.apps.users.entities.users import User as UserEntity


class CustomerSchema(BaseModel):
    id: int
    first_name: str | None
    last_name: str | None
    email: str | None
    phone: str
    telegram: str | None
    role: str
    balance: float

    @staticmethod
    def from_entity(entity: UserEntity) -> 'CustomerSchema':
        return CustomerSchema(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            email=entity.email,
            phone=entity.phone,
            telegram=entity.telegram,
            role=entity.role,
            balance=entity.balance,
        )
