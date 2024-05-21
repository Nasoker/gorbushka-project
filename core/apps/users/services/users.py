from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.customers.filters import CustomerFilters
from core.apps.users.entities.users import User
from core.apps.users.models import User as UserModel


class BaseCustomersService(ABC):
    @abstractmethod
    def get_customers(self, filters: CustomerFilters, pagination: PaginationIn) -> Iterable[User]:
        ...

    @abstractmethod
    def get_customers_count(self, filters: CustomerFilters) -> int:
        ...

    @abstractmethod
    def get_customer(self, customer_id: int) -> User:
        ...


class ORMCustomersService(BaseCustomersService):
    def get_customers(self, filters: CustomerFilters, pagination: PaginationIn) -> Iterable[User]:
        query = self._build_customers_query(filters)
        qs = UserModel.objects.filter(query)[pagination.offset:pagination.offset + pagination.limit]

        return [user.to_entity() for user in qs]

    def get_customers_count(self, filters: CustomerFilters) -> int:
        query = self._build_customers_query(filters)
        return UserModel.objects.filter(query).count()

    def get_customer(self, customer_id: int) -> User | None:
        # TODO: changed to  ||| & Q(role='Customer') ||| or smth
        qs = UserModel.objects.filter(Q(pk=customer_id))

        users = [user.to_entity() for user in qs]

        if users:
            return users[0]

        return None

    def _build_customers_query(self, filters: CustomerFilters) -> Q:
        query = Q()
        query &= Q(role='Customer')

        if filters.name is not None:
            query &= Q(first_name__icontains=filters.name) | Q(last_name__icontains=filters.name)

        return query
