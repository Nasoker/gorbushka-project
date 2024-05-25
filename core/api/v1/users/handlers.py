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
from core.api.v1.users.schemas import UserOutSchema
from core.apps.users.services.users import (
    BaseUserService,
    ORMUserService,
)


router = Router(tags=['Users'])


@router.get('', response=ApiResponse[ListPaginatedResponse[UserOutSchema]])
def get_users_handler(
        request: HttpRequest,
        filters: Query[UserFilters],
        pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[UserOutSchema]]:
    service: BaseUserService = ORMUserService()

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
    service: BaseUserService = ORMUserService()

    user = service.get_user(user_id=user_id)

    if not user:
        raise HttpError(status_code=404, message=f'User with id: {user_id} not found')

    return ApiResponse(data=UserOutSchema.from_entity(user))
