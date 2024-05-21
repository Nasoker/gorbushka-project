import decimal
from abc import (
    ABC,
    abstractmethod,
)
from datetime import datetime
from typing import Iterable

from django.db.models import (
    F,
    Q,
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
    def create_or_update_transaction(self, transaction: Transaction) -> Transaction:
        ...

    @abstractmethod
    def get_transaction_type(self, transaction_type: str) -> TransactionType | None:
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

    def create_or_update_transaction(self, transaction: Transaction) -> Transaction:
        if transaction.id:
            updated_rows_amount = TransactionModel.objects.filter(Q(pk=transaction.id)).update(
                updated_at=datetime.now(),
                amount=transaction.amount,
                client_balance=F('client_balance') + (decimal.Decimal(transaction.amount) - F('amount')),
                comment=transaction.comment,
                provider=transaction.provider,
            )

            if updated_rows_amount == 0:
                raise Exception(f'Transaction with id {transaction.id} was not updated')

            return TransactionModel.objects.filter(Q(pk=transaction.id))[0].to_entity()
        else:
            transaction_type = self.get_transaction_type(transaction.transaction_type)

            if not transaction_type:
                # TODO: check exception
                raise Exception(f'There is no transaction type: {transaction.transaction_type}')

            transaction.transaction_type_id = transaction_type.id
            transaction_dto: TransactionModel = TransactionModel.from_entity(transaction)
            transaction_dto.save()

            return transaction_dto.to_entity()

    def get_transaction_type(self, transaction_type: str) -> TransactionType | None:
        qs = TransactionTypeModel.objects.filter(Q(type=transaction_type))

        transaction_types = [transaction_type.to_entity() for transaction_type in qs]

        if transaction_types:
            return transaction_types[0]

        return None

    def _build_transactions_query(self, filters: TransactionFilters) -> Q:
        query = Q()

        if filters.client_id is not None:
            query &= Q(client_id=filters.client_id)

        return query
