from django.http import HttpRequest
from ninja import (
    Query,
    Router,
)
from ninja.errors import HttpError

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
    CreateTransactionInSchema,
    TransactionOutSchema,
    TransactionsTotalOutSchema,
    TransactionSubtotalOutSchema,
    TransactionTypeOutSchema,
    UpdateTransactionInSchema,
)
from core.apps.transactions.services.transactions import (
    BaseTransactionsService,
    ORMTransactionsService,
)
from core.apps.users.services.users import (
    BaseUsersService,
    ORMUsersService,
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


@router.post('', response=ApiResponse[TransactionOutSchema])
def create_transaction_handler(
        request: HttpRequest,
        transaction_in: CreateTransactionInSchema,
) -> ApiResponse[TransactionOutSchema]:
    user_service: BaseUsersService = ORMUsersService()
    transaction_service: BaseTransactionsService = ORMTransactionsService()

    customer = None
    if transaction_in.customer_id:
        customer = user_service.get_user(transaction_in.customer_id)

        if not customer:
            raise HttpError(status_code=400, message=f'Customer with id: {transaction_in.customer_id} not found')

    transaction_type = transaction_service.get_transaction_type_by_id(transaction_in.transaction_type_id)

    if not transaction_type:
        raise HttpError(
            status_code=400,
            message=f'Transaction type with id: {transaction_in.transaction_type_id} not found',
        )

    transaction_entity = transaction_in.to_entity(customer, transaction_type)

    saved_transaction = transaction_service.create_transaction(transaction_entity)

    return ApiResponse(data=TransactionOutSchema.from_entity(saved_transaction))


@router.get('/debts', response=ApiResponse[TransactionsTotalOutSchema])
def get_debts_handler(
        request: HttpRequest,
) -> ApiResponse[TransactionsTotalOutSchema]:
    service: BaseTransactionsService = ORMTransactionsService()

    debts = service.get_debts()

    return ApiResponse(data=TransactionsTotalOutSchema(total=debts))


@router.get('/total', response=ApiResponse[TransactionsTotalOutSchema])
def get_transactions_total_handler(
        request: HttpRequest,
        filters: Query[TransactionFilters],
):
    service: BaseTransactionsService = ORMTransactionsService()

    try:
        total = service.get_transactions_total(filters=filters)
        return ApiResponse(data=TransactionsTotalOutSchema(total=total))
    except Exception as e:
        # TODO: add logging ???
        print(e)


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


@router.get('/{customer_id}', response=ApiResponse[ListPaginatedResponse[TransactionOutSchema]])
def get_customer_transactions_handler(
        request: HttpRequest,
        customer_id: int,
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[TransactionOutSchema]]:
    service: BaseTransactionsService = ORMTransactionsService()

    transactions = service.get_customer_transactions(customer_id=customer_id, pagination=pagination_in)
    transactions_count = service.get_customer_transactions_count(customer_id=customer_id)

    items = [TransactionOutSchema.from_entity(obj) for obj in transactions]
    pagination_out = PaginationOut(offset=pagination_in.offset, limit=pagination_in.limit, total=transactions_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.put('/{transaction_id}/update', response=ApiResponse[TransactionOutSchema])
def update_transaction_handler(
        request: HttpRequest,
        transaction_id: int,
        transaction_in: UpdateTransactionInSchema,
) -> ApiResponse[TransactionOutSchema]:
    service: BaseTransactionsService = ORMTransactionsService()

    transaction = service.get_transaction_by_id(transaction_id)

    if not transaction:
        raise HttpError(status_code=400, message=f'Transaction with id: {transaction_id} not found')

    updated_transaction = service.update_transaction(transaction_id, transaction_in.dict())

    return ApiResponse(data=TransactionOutSchema.from_entity(updated_transaction))


@router.get('/{transaction_id}/subtotal', response=ApiResponse[TransactionSubtotalOutSchema])
def get_subtotal_handler(
        request: HttpRequest,
        transaction_id: int,
) -> ApiResponse[TransactionSubtotalOutSchema]:
    service: BaseTransactionsService = ORMTransactionsService()

    try:
        subtotal = service.get_subtotal(transaction_id=transaction_id)
    except Exception:
        raise HttpError(status_code=400, message=f'Customer transaction with id: {transaction_id} not found')

    return ApiResponse(data=TransactionSubtotalOutSchema(subtotal=subtotal))
