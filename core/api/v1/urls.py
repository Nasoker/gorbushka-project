from ninja import Router

from core.api.v1.transactions.handlers import router as transactions_router
from core.api.v1.users.handlers import router as users_router


router = Router(tags=['v1'])
router.add_router(router=users_router, prefix='users/')
router.add_router(router=transactions_router, prefix='transactions/')
