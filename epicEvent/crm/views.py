from rest_framework import viewsets,permissions,generics
from django.shortcuts import get_object_or_404
from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from authentication.permissions import IsCommercialUser,ManagementOrSuperuserAccess,IsSupportUser,DenyAll,IsCommercial,IsManagement,IsSupport,IsNotCommercial,IsCommercialUserCont,ManagementOnlyAccess
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        
        if self.action in ['create', 'update', 'partial_update']:           
            return [IsCommercialUser()]
             
        if self.action == 'destroy':
            return [DenyAll()]

        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):       
        serializer.save(sales_contact=self.request.user)
    

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            if self.request.user.role == 'management':
                return [ManagementOnlyAccess()]
            elif self.request.user.role == 'commercial':
                return [IsCommercialUserCont()]
            else:
                return [DenyAll()]
        elif self.action == 'destroy':
            return [DenyAll()]
        elif self.action in ['list', 'retrieve']:
            if self.request.user.role == 'support':
                return [IsSupport()]
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated()]
    
    
      
  

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer 
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [IsCommercial]
        elif self.action in ['update', 'partial_update']:
                permission_classes = [IsManagement | IsSupport,IsNotCommercial]
        elif self.action == 'destroy':
            permission_classes = [DenyAll]
        else:            
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]   
    

    def destroy(self, request, *args, **kwargs):        
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
       
    
        
    
class CommercialUnsignedContractsView(generics.ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        
        if self.request.user.is_authenticated and self.request.user.role == 'commercial':
            return Contract.objects.filter(is_signed=False, sales_contact=self.request.user)
        return Contract.objects.none()  
    
class CommercialRemainingAmountContractsView(generics.ListAPIView):
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        
        if self.request.user.is_authenticated and self.request.user.role == 'commercial':
            return Contract.objects.filter(remaining_amount__gt=0, sales_contact=self.request.user)
        return Contract.objects.none() 
    
class NullSupportEventsView(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.filter(support_contact__isnull=True)
    serializer_class = EventSerializer
    permission_classes = [ManagementOrSuperuserAccess]
    
    
class SupportAssignedEventsView(viewsets.ReadOnlyModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsSupportUser]

    def get_queryset(self):        
        return Event.objects.filter(support_contact=self.request.user)
    
