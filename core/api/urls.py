from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from ninja_jwt.authentication import JWTAuth

from django.urls import path

from core.api.v1.transactions.handlers import router as transactions_router
from core.api.v1.customers.handlers import router as customers_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

# TODO: add JWTAuth
api.add_router(router=transactions_router, prefix='transactions', auth=JWTAuth())
api.add_router(router=customers_router, prefix='customers', auth=JWTAuth())

urlpatterns = [
    path("", api.urls),
]
