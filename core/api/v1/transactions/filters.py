from ninja import Schema


class TransactionFilters(Schema):
    customer_id: int | None = None
