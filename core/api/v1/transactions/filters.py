from ninja import Schema


class TransactionFilters(Schema):
    types: list[int] | None = None
    is_income: bool | None = None
    is_current_month: bool | None = None


class BalancesSumFilters(Schema):
    positive: bool | None = True
