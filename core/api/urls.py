from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from ninja_jwt.authentication import JWTAuth

from django.http import HttpRequest
from django.urls import path

from core.api.v1.transactions.handlers import router as transactions_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


@api.get('/ping', auth=JWTAuth())
def ping(request: HttpRequest):
    return 'pong'


# TODO: add JWTAuth
api.add_router(router=transactions_router, prefix='transactions')

urlpatterns = [
    path("", api.urls),
]
