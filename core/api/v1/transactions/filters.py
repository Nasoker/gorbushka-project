from ninja import Schema


class TransactionFilters(Schema):
    types: list[int] | None = None
    is_income: bool | None = None
