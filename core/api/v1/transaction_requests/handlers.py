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
from core.api.v1.transaction_requests.schemas import (
    CreateTransactionRequestInSchema,
    TransactionRequestOutSchema,
    UpdateTransactionRequestInSchema,
)
from core.apps.transactions.services.transaction_requests import (
    BaseTransactionRequestsService,
    ORMTransactionRequestsService,
)
from core.apps.transactions.services.transactions import (
    BaseTransactionsService,
    ORMTransactionsService,
)
from core.apps.users.services.users import (
    BaseUsersService,
    ORMUsersService,
)


router = Router(tags=['Transaction Requests'])


@router.get('', response=ApiResponse[ListPaginatedResponse[TransactionRequestOutSchema]])
def get_transaction_requests_handler(
        request: HttpRequest,
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[TransactionRequestOutSchema]]:
    service: BaseTransactionRequestsService = ORMTransactionRequestsService()
    transaction_requests = service.get_transaction_requests(pagination=pagination_in)
    transaction_requests_count = service.get_transaction_requests_count()

    items = [TransactionRequestOutSchema.from_entity(obj) for obj in transaction_requests]
    pagination__out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=transaction_requests_count,
    )

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination__out))


@router.get('/{transaction_request_id}', response=ApiResponse[TransactionRequestOutSchema])
def get_transaction_request_handler(
        request: HttpRequest,
        transaction_request_id: int,
) -> ApiResponse[TransactionRequestOutSchema]:
    service: BaseTransactionRequestsService = ORMTransactionRequestsService()
    transaction = service.get_transaction_request(transaction_request_id)

    return ApiResponse(data=TransactionRequestOutSchema.from_entity(transaction))


@router.post('', response=ApiResponse[TransactionRequestOutSchema])
def create_transaction_request_handler(
        request: HttpRequest,
        transaction_request_in: CreateTransactionRequestInSchema,
) -> ApiResponse[TransactionRequestOutSchema]:
    user_service: BaseUsersService = ORMUsersService()
    transaction_service: BaseTransactionsService = ORMTransactionsService()
    transaction_requests_service: BaseTransactionRequestsService = ORMTransactionRequestsService()

    customer = None
    if transaction_request_in.customer_id:
        customer = user_service.get_user(transaction_request_in.customer_id)

        if not customer:
            raise HttpError(
                status_code=400,
                message=f'Customer with id: {transaction_request_in.customer_id} not found',
            )

    transaction_type = transaction_service.get_transaction_type_by_id(transaction_request_in.transaction_type_id)
    if not transaction_type:
        raise HttpError(
            status_code=400,
            message=f'Transaction type with id: {transaction_request_in.transaction_type_id} not found',
        )

    requester = user_service.get_user(transaction_request_in.requester_id)
    if not requester:
        raise HttpError(
            status_code=400,
            message=f'Requester with id: {transaction_request_in.requester_id} not found',
        )

    transaction_request_entity = transaction_request_in.to_entity(transaction_type, requester, customer)
    saved_transaction_request = transaction_requests_service.create_transaction_request(transaction_request_entity)

    return ApiResponse(data=TransactionRequestOutSchema.from_entity(saved_transaction_request))


@router.put('/{transaction_request_id}', response=ApiResponse[TransactionRequestOutSchema])
def update_transaction_request_handler(
        request: HttpRequest,
        transaction_request_id: int,
        transaction_request_in: UpdateTransactionRequestInSchema,
) -> ApiResponse[TransactionRequestOutSchema]:
    service: BaseTransactionRequestsService = ORMTransactionRequestsService()

    transaction_request = service.get_transaction_request(transaction_request_id)
    if not transaction_request:
        raise HttpError(status_code=400, message=f'Transaction Request with id: {transaction_request_id} not found')

    # TODO: check if we can update Customer
    updated_transaction = service.update_transaction_request(
        transaction_request_id,
        transaction_request_in.model_dump(),
    )

    return ApiResponse(data=TransactionRequestOutSchema.from_entity(updated_transaction))


@router.post('/{transaction_request_id}/approve', response=ApiResponse[TransactionRequestOutSchema])
def approve_transaction_request_handler(
        request: HttpRequest,
        transaction_request_id: int,
        approver_id: int,
) -> ApiResponse[TransactionRequestOutSchema]:
    service: BaseTransactionRequestsService = ORMTransactionRequestsService()
    service.approve_transaction_request(transaction_request_id, approver_id)
    # TODO: what can we return here ??? (Maybe created transaction)


@router.post('/{transaction_request_id}/reject', response=ApiResponse[TransactionRequestOutSchema])
def reject_transaction_request_handler(
        request: HttpRequest,
        transaction_request_id: int,
        approver_id: int,
) -> ApiResponse:
    service: BaseTransactionRequestsService = ORMTransactionRequestsService()
    service.reject_transaction_request(transaction_request_id, approver_id)

    return ApiResponse(data='Request was rejected successfully')
