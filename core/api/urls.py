from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

from ninja_jwt.authentication import JWTAuth

from django.http import HttpRequest
from django.urls import path

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)


@api.get('/ping', auth=JWTAuth())
def ping(request: HttpRequest):
    return 'pong'


urlpatterns = [
    path("", api.urls),
]
