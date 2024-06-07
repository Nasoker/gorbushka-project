from abc import (
    ABC,
    abstractmethod,
)
from typing import Iterable

from django.db.models import (
    Q,
    Sum,
)

from core.api.filters import PaginationIn
from core.api.v1.transactions.filters import TransactionFilters
from core.apps.transactions.entities.transactions import (
    Transaction as Transaction,
    TransactionType as TransactionType,
)
from core.apps.transactions.models import (
    Transaction as TransactionModel,
    TransactionType as TransactionTypeModel,
)


class BaseTransactionsService(ABC):
    @abstractmethod
    def get_transactions(self, filters: TransactionFilters, pagination: PaginationIn) -> Iterable[Transaction]:
        ...

    @abstractmethod
    def get_transactions_count(self, filters: TransactionFilters) -> int:
        ...

    @abstractmethod
    def get_transactions_total(self, filters: TransactionFilters) -> float:
        ...

    @abstractmethod
    def get_customer_transactions(self, customer_id: int, pagination: PaginationIn) -> Iterable[Transaction]:
        ...

    @abstractmethod
    def get_customer_transactions_count(self, customer_id: int) -> int:
        ...

    @abstractmethod
    def get_user_balance(self, user_id: int) -> float:
        ...

    @abstractmethod
    def get_transaction_types(self, pagination: PaginationIn) -> Iterable[TransactionType]:
        ...

    @abstractmethod
    def get_transaction_types_count(self) -> int:
        ...


class ORMTransactionsService(BaseTransactionsService):
    def get_transactions(self, filters: TransactionFilters, pagination: PaginationIn) -> Iterable[Transaction]:
        query = self._build_transactions_query(filters)
        qs = TransactionModel \
                 .objects \
                 .filter(query) \
                 .order_by('-created_at') \
                 .select_related()[pagination.offset:pagination.offset + pagination.limit]

        return [transaction.to_entity() for transaction in qs]

    def get_transactions_count(self, filters: TransactionFilters) -> int:
        query = self._build_transactions_query(filters)
        return TransactionModel.objects.filter(query).count()

    def get_transactions_total(self, filters: TransactionFilters) -> float:
        query = self._build_transactions_query(filters)
        total_data = TransactionModel.objects.filter(query).aggregate(Sum('amount'))

        if total_data['amount__sum']:
            return total_data['amount__sum']
        else:
            return 0

    def get_customer_transactions(self, customer_id: int, pagination: PaginationIn) -> Iterable[Transaction]:
        qs = TransactionModel \
                 .objects \
                 .filter(customer__pk=customer_id) \
                 .order_by('-created_at') \
                 .select_related()[pagination.offset:pagination.offset + pagination.limit]

        return [transaction.to_entity() for transaction in qs]

    def get_customer_transactions_count(self, customer_id: int) -> int:
        return TransactionModel.objects.filter(customer__pk=customer_id).count()

    def get_user_balance(self, user_id: int) -> float:
        balance_data = TransactionModel.objects.filter(Q(customer__pk=user_id)).aggregate(Sum('amount'))

        if balance_data['amount__sum']:
            return balance_data['amount__sum']
        else:
            return 0

    def get_transaction_types(self, pagination: PaginationIn) -> Iterable[TransactionType]:
        qs = TransactionTypeModel.objects.all()[pagination.offset:pagination.offset + pagination.limit]
        return [transaction_type.to_entity() for transaction_type in qs]

    def get_transaction_types_count(self) -> int:
        return TransactionTypeModel.objects.all().count()

    def _build_transactions_query(self, filters: TransactionFilters) -> Q:
        query = Q()

        if filters.types is not None:
            for type_id in filters.types:
                query |= Q(transaction_type__pk=type_id)

        if filters.is_income is not None:
            if filters.is_income:
                query &= Q(amount__gte=0)
            else:
                query &= Q(amount__lt=0)

        return query
