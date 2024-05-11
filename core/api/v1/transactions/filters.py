from ninja import Schema


class TransactionFilters(Schema):
    client_id: int | None = None
