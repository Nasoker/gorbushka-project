from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)

from core.api.filters import (
    PaginationIn,
    PaginationOut,
)
from core.api.schemas import (
    ApiResponse,
    ListPaginatedResponse,
)
from core.api.v1.transactions.filters import TransactionFilters
from core.api.v1.transactions.schemas import (
    TransactionInSchema,
    TransactionOutSchema,
    TransactionTypeOutSchema,
)
from core.apps.transactions.services.transactions import (
    BaseTransactionsService,
    ORMTransactionsService,
)


router = Router(tags=['Transactions'])


@router.get('', response=ApiResponse[ListPaginatedResponse[TransactionOutSchema]])
def get_transactions_handler(
        request: HttpRequest,
        filters: Query[TransactionFilters],
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[TransactionOutSchema]]:
    service: BaseTransactionsService = ORMTransactionsService()

    transactions = service.get_transactions(filters=filters, pagination=pagination_in)
    transactions_count = service.get_transactions_count(filters=filters)

    items = [TransactionOutSchema.from_entity(obj) for obj in transactions]
    pagination_out = PaginationOut(offset=pagination_in.offset, limit=pagination_in.limit, total=transactions_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('/transaction_types', response=ApiResponse[ListPaginatedResponse[TransactionTypeOutSchema]])
def get_transaction_types_handler(
        request: HttpRequest,
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[TransactionTypeOutSchema]]:
    service: BaseTransactionsService = ORMTransactionsService()

    transaction_types = service.get_transaction_types(pagination=pagination_in)
    transaction_types_count = service.get_transaction_types_count()

    items = [TransactionTypeOutSchema.from_entity(obj) for obj in transaction_types]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=transaction_types_count,
    )

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.post('upsert', response=ApiResponse[TransactionOutSchema])
def create_transaction_handler(
        request: HttpRequest,
        transaction_in: TransactionInSchema,
) -> ApiResponse[TransactionOutSchema]:
    service: BaseTransactionsService = ORMTransactionsService()

    transaction = service.create_or_update_transaction(transaction_in.to_entity())

    return ApiResponse(data=TransactionOutSchema.from_entity(transaction))
