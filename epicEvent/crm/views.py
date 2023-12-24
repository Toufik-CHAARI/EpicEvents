from rest_framework import viewsets,permissions,generics
from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from authentication.permissions import IsCommercialUser,CommercialUpdateAssignedOrManagementFullAccess,ManagementOrSuperuserAccess,IsSupportUser


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    
    def get_permissions(self):
        
        if self.action == 'create':
           
            return [IsCommercialUser()]
        elif self.action in ['update', 'partial_update']:            
            return [ManagementOrSuperuserAccess()]        
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):       
        serializer.save(sales_contact=self.request.user)
    

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    def get_permissions(self):        
        if self.action in ['create', 'update', 'partial_update', 'destroy']:            
            if self.request.user.is_superuser or self.request.user.role == 'management':
                return [ManagementOrSuperuserAccess()]
           
            elif self.request.user.role == 'commercial':
                return [CommercialUpdateAssignedOrManagementFullAccess()]
            else:
               
                return [permissions.IsAdminUser()]
        
        
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        
        return Contract.objects.all()
    
    
      
    
    

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer    
    #permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [IsCommercialUser]
    def get_permissions(self):
        if self.request.user.is_superuser or self.request.user.role == 'management':
            return [ManagementOrSuperuserAccess()]        
        elif self.request.user.role == 'support':           
            if self.action in ['update', 'partial_update']:
                return [IsSupportUser()]            
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.IsAuthenticated()]
    def get_queryset(self):    
        return super().get_queryset()
    
        
    
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