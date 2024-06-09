from abc import (
    ABC,
    abstractmethod,
)

from ninja import File

from core.apps.receipts.entities.receipts import Receipt
from core.apps.receipts.models import Receipt as ReceiptModel


class BaseReceiptService(ABC):
    @abstractmethod
    def get_receipt(self, transaction_id: int) -> Receipt:
        ...

    @abstractmethod
    def save_receipt(self, transaction_id: int, file: File) -> Receipt:
        ...


class ORMReceiptService(BaseReceiptService):
    def get_receipt(self, transaction_id: int) -> Receipt | None:
        receipt = ReceiptModel.objects.filter(transaction_id=transaction_id).first()

        if receipt:
            return receipt.to_entity()

        return None

    def save_receipt(self, transaction_id: int, file: File) -> Receipt:
        receipt = ReceiptModel.objects.filter(transaction_id=transaction_id).first()

        if receipt is None:
            receipt = ReceiptModel.objects.create(
                transaction_id=transaction_id,
                file=file,
            )
        else:
            receipt.file = file
            receipt.save()

        return receipt.to_entity()
