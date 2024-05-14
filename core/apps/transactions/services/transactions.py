from abc import ABC, abstractmethod
from typing import Iterable

from django.db.models import Q

from core.api.filters import PaginationIn
from core.api.v1.transactions.filters import TransactionFilters
from core.apps.transactions.entities.transactions import Transaction as Transaction
from core.apps.transactions.models import Transaction as TransactionModel


class BaseTransactionsService(ABC):
    @abstractmethod
    def get_transactions(self, filters: TransactionFilters, pagination: PaginationIn) -> Iterable[Transaction]:
        ...

    @abstractmethod
    def get_transactions_count(self, filters: TransactionFilters) -> int:
        ...


class ORMTransactionsService(BaseTransactionsService):
    def get_transactions(self, filters: TransactionFilters, pagination: PaginationIn) -> Iterable[Transaction]:
        query = self._build_transactions_query(filters)
        qs = TransactionModel \
                 .objects \
                 .filter(query) \
                 .order_by('-created_at')[pagination.offset:pagination.offset + pagination.limit]

        return [transaction.to_entity() for transaction in qs]

    def get_transactions_count(self, filters: TransactionFilters) -> int:
        query = self._build_transactions_query(filters)
        return TransactionModel.objects.filter(query).count()

    def _build_transactions_query(self, filters: TransactionFilters) -> Q:
        query = Q()

        if filters.client_id is not None:
            # TODO: check icontains for search
            query &= Q(client_id=filters.client_id)

        return query
