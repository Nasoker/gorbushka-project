from django.http import HttpRequest
from ninja import (
    File,
    Router,
)
from ninja.errors import HttpError
from ninja.files import UploadedFile

from core.api.schemas import ApiResponse
from core.api.v1.receipts.schemas import ReceiptOutSchema
from core.apps.receipts.services.receipts import (
    BaseReceiptService,
    ORMReceiptService,
)


router = Router(tags=['Receipts'])


@router.get('/{transaction_id}', response=ApiResponse[ReceiptOutSchema])
def handle_get_receipt(
        request: HttpRequest,
        transaction_id: int,
) -> ApiResponse[ReceiptOutSchema]:
    service: BaseReceiptService = ORMReceiptService()

    try:
        receipt = service.get_receipt(transaction_id)

        if receipt is None:
            raise HttpError(status_code=400, message=f'No receipt found for transaction: {transaction_id}')

        return ApiResponse(data=ReceiptOutSchema.from_entity(receipt))
    except Exception:
        raise HttpError(status_code=500, message='Something went wrong. Please try again.')


@router.post('/{transaction_id}/save', response=ApiResponse[ReceiptOutSchema])
def handle_add_receipt(
        request: HttpRequest,
        transaction_id: int,
        file: UploadedFile = File(...),
) -> ApiResponse[ReceiptOutSchema]:
    service: BaseReceiptService = ORMReceiptService()

    try:
        saved_receipt = service.save_receipt(transaction_id=transaction_id, file=file)
        return ApiResponse(data=ReceiptOutSchema.from_entity(saved_receipt))
    except Exception as e:
        print(e)
        raise HttpError(status_code=500, message='Something went wrong. Please try again.')
