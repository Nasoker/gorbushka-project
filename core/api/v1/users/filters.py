from ninja import Schema


class UserFilters(Schema):
    name: str | None = None
