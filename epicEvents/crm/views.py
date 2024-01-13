from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import NotFound
from .models import Client, Contract, Event
from authentication.models import CustomUser
from .serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)
from authentication.permissions import (
    IsCommercialUser,
    ManagementOrSuperuserAccess,
    IsSupportUser,
    DenyAll,
    IsCommercial,
    IsManagement,
    IsSupport,
    IsNotCommercial,
    IsCommercialUserCont,
    ManagementOnlyAccess,
)
from rest_framework.response import Response
from rest_framework import status


class ClientViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling requests related to the Client model.

    The 'get_permissions' method customizes access control based on
    the action being performed:
    -For 'list' and 'retrieve' actions, any authenticated user
    is allowed.
    -For 'create', 'update', and 'partial_update', only commercial
    users are allowed through IsCommercialUser.
    - For 'destroy', access is denied to all users via DenyAll.
    'perform_create' is overridden to set the 'sales_contact' field
    to the current user automatically upon creation.
    """

    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]

        if self.action in ["create", "update", "partial_update"]:
            return [IsCommercialUser()]

        if self.action == "destroy":
            return [DenyAll()]

        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(sales_contact=self.request.user)


class ContractViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling requests related to the Contract model.
    The 'get_permissions' method defines custom access controls based
    actions performed and the user's role:
    - For actions 'create', 'update', and 'partial_update':
    - Users with a 'management' role are granted access via
    the ManagementOnlyAccess permission.
    - Users with a 'commercial' role are are granted access via
    IsCommercialUserCont permission.
    - All other users are denied access through the DenyAll
    permission.
    - For the 'destroy' action, all users are denied access
    regardless of their role, using the DenyAll permission.
    - For all other actions, including 'list' and 'retrieve', access
    is granted to any authenticated user, ensuring that every authenticated
    user can view and retrieve Contract records."""

    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update"]:
            if self.request.user.role == "management":
                return [ManagementOnlyAccess()]
            elif self.request.user.role == "commercial":
                return [IsCommercialUserCont()]
            else:
                return [DenyAll()]
        elif self.action == "destroy":
            return [DenyAll()]
        else:
            return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        sales_contact_id = serializer.validated_data.get(
            "sales_contact"
        )

        # Check if the sales_contact user exists
        if sales_contact_id:
            try:
                sales_contact = CustomUser.objects.get(
                    id=sales_contact_id.id
                )
            except CustomUser.DoesNotExist:
                raise NotFound(
                    detail="Sales contact user does not exist."
                )

            # Check if the user's role is 'commercial'
            if sales_contact.role != "commercial":
                return Response(
                    {
                        "detail": "user must have the role of commercial."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer.save()


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    """
    Viewset for handling requests related to the Event model.
    Methods:
    - The get_permissions method allows any authenticated user
    to list and retrieve events, only commercial users can create
    events, management or support users (excluding commercial users)
    can perform updates and partial updates, and denies to all users
    the ability to delete events.
    """

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == "create":
            permission_classes = [IsCommercial]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [
                IsManagement | IsSupport,
                IsNotCommercial,
            ]
        elif self.action == "destroy":
            permission_classes = [DenyAll]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommercialUnsignedContractsView(generics.ListAPIView):
    """
    View for listing all unsigned contracts associated with the
    commercial user.Returns an empty queryset if the user is not
    a commercial user.
    """

    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.role == "commercial"
        ):
            return Contract.objects.filter(
                is_signed=False, sales_contact=self.request.user
            )
        return Contract.objects.none()


class CommercialRemainingAmountContractsView(generics.ListAPIView):
    """
    View for listing all contracts with a remaining amount greater than zero
    associated with the commercial user.
    Provides an empty queryset if the user is not a commercial user.
    """

    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if (
            self.request.user.is_authenticated
            and self.request.user.role == "commercial"
        ):
            return Contract.objects.filter(
                remaining_amount__gt=0, sales_contact=self.request.user
            )
        return Contract.objects.none()


class NullSupportEventsView(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for listing events without an assigned support contact.
    Access limited to management users or superusers through
    ManagementOrSuperuserAccess.
    """

    queryset = Event.objects.filter(support_contact__isnull=True)
    serializer_class = EventSerializer
    permission_classes = [ManagementOrSuperuserAccess]


class SupportAssignedEventsView(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for listing events that are assigned to the logged-in support user.
    Access restricted to authenticated users with the 'support' role
    via the "IsSupportUser" permission class.
    """

    serializer_class = EventSerializer
    permission_classes = [IsSupportUser]

    def get_queryset(self):
        return Event.objects.filter(support_contact=self.request.user)
