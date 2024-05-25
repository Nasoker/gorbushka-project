from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import (
    Q,
    Value,
)
from django.db.models.functions import Concat

from core.api.filters import PaginationIn
from core.api.v1.users.filters import UserFilters
from core.apps.users.entities.users import User
from core.apps.users.models import User as UserModel


class BaseUserService(ABC):
    @abstractmethod
    def get_users(self, filters: UserFilters, pagination: PaginationIn) -> Iterable[User]:
        ...

    @abstractmethod
    def get_users_count(self, filters: UserFilters) -> int:
        ...

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        ...


class ORMUserService(BaseUserService):
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

        if users:
            return users[0]

        return None

    def _build_users_query(self, filters: UserFilters) -> Q:
        query = Q()

        if filters.is_customer:
            query &= Q(role='Customer')

        # TODO: is it a good way to go?
        if filters.is_employee:
            query &= Q(role='Cashier') | Q(role='Moderator') | Q(role='Admin')

        if filters.name is not None:
            query &= (
                Q(full_name__icontains=filters.name)
                | Q(first_name__icontains=filters.name)
                | Q(last_name__icontains=filters.name)
            )

        return query
