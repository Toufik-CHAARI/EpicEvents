from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,
    ContractViewSet,
    EventViewSet,
)

router = DefaultRouter()
router.register(r"client", ClientViewSet)
router.register(r"contract", ContractViewSet)
router.register(r"event", EventViewSet)


urlpatterns = [
    path("", include(router.urls)),
]