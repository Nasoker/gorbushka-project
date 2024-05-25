from ninja import Schema


class UserFilters(Schema):
    name: str | None = None
    is_customer: bool | None = None
    is_employee: bool | None = None
