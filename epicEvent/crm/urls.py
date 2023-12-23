from django.urls import path, include
from .views import CommercialUnsignedContractsView,CommercialRemainingAmountContractsView,NullSupportEventsView
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
router.register(r'null-role-events', NullSupportEventsView, basename='null-role-events')


urlpatterns = [
    path("", include(router.urls)),
    path('contracts/commercial/unsigned/', CommercialUnsignedContractsView.as_view(), name='commercial-unsigned-contracts'),
    path('contracts/commercial/remaining-amount/', CommercialRemainingAmountContractsView.as_view(), name='commercial-remaining-amount-contracts'),
]
