from rest_framework import generics,permissions
from crm.models import Contract
from crm.serializers import ContractSerializer


class IsCommercialUser(permissions.BasePermission):
    def has_permission(self, request, view):        
        return request.user.is_authenticated and request.user.role == 'commercial'

    def has_object_permission(self, request, view, obj):        
        if view.action in ['update', 'partial_update']:
            if hasattr(obj, 'sales_contact'):
                return obj.sales_contact == request.user
            elif hasattr(obj, 'client'):  
                return obj.client.sales_contact == request.user
        return True  
    
class CommercialUpdateAssignedOrManagementFullAccess(permissions.BasePermission):
    def has_permission(self, request, view):        
        if request.user.is_superuser or request.user.role == 'management':
            return True
        elif request.user.role == 'commercial':
            return view.action in ['list', 'retrieve', 'update', 'partial_update']
        return False

    def has_object_permission(self, request, view, obj):        
        if request.user.role == 'commercial' and view.action in ['update', 'partial_update']:
            return obj.client.sales_contact == request.user
        return True 
    


    
