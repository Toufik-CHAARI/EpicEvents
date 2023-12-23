from rest_framework import viewsets,permissions,generics
from .models import Client, Contract, Event
from .serializers import ClientSerializer, ContractSerializer, EventSerializer
from authentication.permissions import IsCommercialUser,CommercialUpdateAssignedOrManagementFullAccess


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsCommercialUser]
     
    
    
    def perform_create(self, serializer):       
        serializer.save(sales_contact=self.request.user)
    

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsCommercialUser]
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [permissions.IsAdminUser()]  
        return [CommercialUpdateAssignedOrManagementFullAccess()]

    def get_queryset(self):        
        if self.request.user.role == 'commercial':
            return Contract.objects.all()
        return super().get_queryset()   
    
    

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = [IsCommercialUser]

    
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