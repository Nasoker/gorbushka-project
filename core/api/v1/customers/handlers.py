from django.http import HttpRequest, HttpResponse
from ninja import Router, Query

from core.api.filters import PaginationIn, PaginationOut
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.customers.filters import CustomerFilters
from core.api.v1.customers.schemas import CustomerSchema
from core.apps.users.services.users import BaseCustomersService, ORMCustomersService

router = Router(tags=['Customers'])


@router.get('/get_customers', response=ApiResponse[ListPaginatedResponse[CustomerSchema]])
def get_customers_handler(
        request: HttpRequest,
        filters: Query[CustomerFilters],
        pagination_in: Query[PaginationIn]
) -> ApiResponse[ListPaginatedResponse[CustomerSchema]]:
    service: BaseCustomersService = ORMCustomersService()

    customers = service.get_customers(filters=filters, pagination=pagination_in)
    customers_count = service.get_customers_count(filters=filters)

    items = [CustomerSchema.from_entity(obj) for obj in customers]
    pagination_out = PaginationOut(offset=pagination_in.offset, limit=pagination_in.limit, total=customers_count)

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('', response=ApiResponse[CustomerSchema])
def get_customer_handler(
        request: HttpRequest,
        customer_id: int
) -> ApiResponse[CustomerSchema]:
    # TODO: do we really need this code ???
    if (customer_id is None or customer_id == '') and request.user is None:
        return ApiResponse(errors=['Customer Id should not be empty'])

    # TODO: add auth checks

    service: BaseCustomersService = ORMCustomersService()
    user_id = customer_id if customer_id is not None else request.user.id
    customer = service.get_customer(customer_id=user_id)

    if customer is None:
        return ApiResponse(errors=[f'There is no customers with Id: {customer_id}'])

    customer_response_data = CustomerSchema.from_entity(customer)

    return ApiResponse(data=customer_response_data)
