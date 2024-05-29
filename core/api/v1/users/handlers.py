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
from core.api.v1.users.filters import UserFilters
from core.api.v1.users.schemas import (
    UserBalanceOutSchema,
    UserOutSchema,
)
from core.apps.transactions.services.transactions import (
    BaseTransactionsService,
    ORMTransactionsService,
)
from core.apps.users.exceptions.exceptions import (
    InvalidUserRoleError,
    UserNotFoundError,
)
from core.apps.users.services.users import (
    BaseUsersService,
    ORMUsersService,
)


router = Router(tags=['Users'])


@router.get('', response=ApiResponse[ListPaginatedResponse[UserOutSchema]])
def get_users_handler(
        request: HttpRequest,
        filters: Query[UserFilters],
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[UserOutSchema]]:
    service: BaseUsersService = ORMUsersService()

    users = service.get_users(filters=filters, pagination=pagination_in)
    users_count = service.get_users_count(filters=filters)

    items = [UserOutSchema.from_entity(obj) for obj in users]
    pagination_out: PaginationOut = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=users_count,
    )

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('/{user_id}', response=ApiResponse[UserOutSchema])
def get_user_handler(
        request: HttpRequest,
        user_id: int,
) -> ApiResponse[UserOutSchema]:
    service: BaseUsersService = ORMUsersService()

    try:
        user = service.get_user(user_id=user_id)
        return ApiResponse(data=UserOutSchema.from_entity(user))
    except UserNotFoundError:
        raise HttpError(status_code=400, message=f'User with id: {user_id} not found')


@router.get('/{user_id}/balance', response=ApiResponse[UserBalanceOutSchema])
def get_user_balance_handler(
        request: HttpRequest,
        user_id: int,
) -> ApiResponse[UserBalanceOutSchema]:
    users_service: BaseUsersService = ORMUsersService()
    transactions_service: BaseTransactionsService = ORMTransactionsService()

    try:
        user = users_service.get_user(user_id=user_id)

        if user.role != 'Customer':
            raise InvalidUserRoleError()

        balance = transactions_service.get_user_balance(user_id)

        return ApiResponse(data=UserBalanceOutSchema(id=user_id, balance=balance))
    except UserNotFoundError:
        raise HttpError(status_code=400, message=f'User with id: {user_id} not found')
    except InvalidUserRoleError:
        raise HttpError(status_code=400, message='Balance is only available for customers')
