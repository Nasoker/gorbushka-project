from ninja import Schema


class CustomerFilters(Schema):
    name: str | None = None
