from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import (
    Q,
    Sum,
    Value,
)
from django.db.models.functions import Concat

from core.api.filters import PaginationIn
from core.api.v1.users.filters import (
    CustomerFilters,
    UserFilters,
)
from core.apps.users.entities.users import (
    Customer,
    Employee,
    User,
)
from core.apps.users.exceptions.exceptions import UserNotFoundError
from core.apps.users.models import User as UserModel


class BaseUsersService(ABC):
    @abstractmethod
    def get_users(self, filters: UserFilters, pagination: PaginationIn) -> Iterable[User]:
        ...

    @abstractmethod
    def get_users_count(self, filters: UserFilters) -> int:
        ...

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        ...

    @abstractmethod
    def get_customers(self, filters: CustomerFilters, pagination: PaginationIn) -> Iterable[Customer]:
        ...

    @abstractmethod
    def get_customers_count(self, filters: CustomerFilters) -> int:
        ...

    @abstractmethod
    def get_employees(self, filters: UserFilters, pagination: PaginationIn) -> Iterable[Employee]:
        ...

    @abstractmethod
    def get_employees_count(self, filters: UserFilters) -> int:
        ...


class ORMUsersService(BaseUsersService):
    def get_users(self, filters: UserFilters, pagination: PaginationIn) -> Iterable[User]:
        query = self._build_users_query(filters)
        qs = UserModel \
                 .objects \
                 .annotate(full_name=Concat('first_name', Value(' '), 'last_name')) \
                 .filter(query)[pagination.offset:pagination.offset + pagination.limit]

        return [user.to_entity() for user in qs]

    def get_users_count(self, filters: UserFilters) -> int:
        query = self._build_users_query(filters)
        return UserModel \
            .objects \
            .annotate(full_name=Concat('first_name', Value(' '), 'last_name')) \
            .filter(query) \
            .count()

    def get_user(self, user_id: int) -> User | None:
        qs = UserModel.objects.filter(Q(pk=user_id))

        users = [user.to_entity() for user in qs]

        if not users:
            raise UserNotFoundError()

        return users[0]

    def get_customers(self, filters: CustomerFilters, pagination: PaginationIn) -> Iterable[Customer]:
        query = self._build_customers_query(filters)
        query &= Q(role='Customer')

        qs = UserModel \
                 .objects \
                 .annotate(full_name=Concat('first_name', Value(' '), 'last_name')) \
                 .annotate(balance=Sum('transaction__amount')) \
                 .filter(query) \
                 .select_related()[pagination.offset:pagination.offset + pagination.limit]

        return [customer.to_customer_entity() for customer in qs]

    def get_customers_count(self, filters: CustomerFilters) -> int:
        query = self._build_customers_query(filters)
        query &= Q(role='Customer')

        return UserModel \
            .objects \
            .annotate(full_name=Concat('first_name', Value(' '), 'last_name')) \
            .annotate(balance=Sum('transaction__amount')) \
            .filter(query) \
            .count()

    def get_employees(self, filters: UserFilters, pagination: PaginationIn) -> Iterable[Employee]:
        query = self._build_users_query(filters)
        query &= (Q(role='Cashier') | Q(role='Moderator') | Q(role='Admin'))

        qs = UserModel \
                 .objects \
                 .annotate(full_name=Concat('first_name', Value(' '), 'last_name')) \
                 .filter(query)[pagination.offset:pagination.offset + pagination.limit]

        return [employee.to_employee_entity() for employee in qs]

    def get_employees_count(self, filters: UserFilters) -> int:
        query = self._build_users_query(filters)
        query &= (Q(role='Cashier') | Q(role='Moderator') | Q(role='Admin'))

        return UserModel \
            .objects \
            .annotate(full_name=Concat('first_name', Value(' '), 'last_name')) \
            .filter(query) \
            .count()

    def _build_users_query(self, filters: UserFilters) -> Q:
        query = Q()

        if filters.name is not None:
            query &= (
                    Q(full_name__icontains=filters.name)
                    | Q(first_name__icontains=filters.name)
                    | Q(last_name__icontains=filters.name)
            )

        return query

    def _build_customers_query(self, filters: CustomerFilters) -> Q:
        query = self._build_users_query(filters)

        if filters.is_debtor is not None:
            if filters.is_debtor:
                query &= Q(balance__lt=0)
            else:
                query &= (Q(balance__gte=0) | Q(balance=None))

        return query
