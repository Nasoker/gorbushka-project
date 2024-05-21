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
    # if request.user.role not in ('Cashier', 'Moderator', 'Admin'):
    #     # TODO: throw unauthorized exception
    #     print(request.user.role)

    service: BaseTransactionsService = ORMTransactionsService()

    transactions = service.get_transactions(filters=filters, pagination=pagination_in)
    transactions_count = service.get_transactions_count(filters=filters)

    items = [TransactionOutSchema.from_entity(obj) for obj in transactions]
    pagination_out = PaginationOut(offset=pagination_in.offset, limit=pagination_in.limit, total=transactions_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.post('/upsert', response=ApiResponse[TransactionOutSchema])
def create_transaction_handler(
        request: HttpRequest,
        transaction_in: TransactionInSchema,
) -> ApiResponse[TransactionOutSchema]:
    service: BaseTransactionsService = ORMTransactionsService()

    transaction = service.create_or_update_transaction(transaction_in.to_entity())

    return ApiResponse(data=TransactionOutSchema.from_entity(transaction))
