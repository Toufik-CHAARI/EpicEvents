from rest_framework import generics,permissions
from crm.models import Contract
from crm.serializers import ContractSerializer
from django.shortcuts import get_object_or_404

class ManagementOnlyAccess(permissions.BasePermission):
    """
    Custom permission to allow only management users full access.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'management'

class IsCommercialUser(permissions.BasePermission):
    def has_permission(self, request, view):        
        
        if not request.user.is_authenticated or request.user.role != 'commercial':
            return False
                
        if view.action in ['list', 'retrieve']:
            return True
        
        if view.action == 'create':
            return True
        
        if view.action in ['update', 'partial_update']:            
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):        
        if view.action in ['update', 'partial_update']:
            if hasattr(obj, 'sales_contact'):
                return obj.sales_contact == request.user
            elif hasattr(obj, 'client'):  
                return obj.client.sales_contact == request.user
        return True  
    def can_create_event(self, request, view):
        # Ensure the request data contains 'contract' and it's a signed contract
        contract_id = request.data.get('contract')
        if contract_id:
            try:
                contract = Contract.objects.get(id=contract_id, is_signed=True)
                return contract.client.sales_contact == request.user
            except Contract.DoesNotExist:
                return False
        return False
    
    
class CommercialUpdateAssignedOrManagementFullAccess(permissions.BasePermission):
    def has_permission(self, request, view):        
        if request.user.is_superuser or request.user.role == 'management':
            return True
        elif request.user.role == 'commercial' and view.action in ['list', 'retrieve']:
            return True
        return False

    def has_object_permission(self, request, view, obj):        
        if view.action in ['update', 'partial_update']:
            return obj.sales_contact == request.user
        return False
    
class ManagementOrSuperuserAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'management'
        )
        
class IsSupportUser(permissions.BasePermission):
    def has_permission(self, request, view):
        
        return request.user.is_authenticated and request.user.role == 'support'

    def has_object_permission(self, request, view, obj):
        
        return obj.support_contact == request.user if view.action in ['update', 'partial_update'] else True
    
class IsCommercialUserCont(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return False
        
        return request.user.is_authenticated and request.user.role == 'commercial'

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'partial_update']:
            return obj.sales_contact == request.user
        return True
    
    
class DenyAll(permissions.BasePermission):
    """
    Custom permission to deny all access.
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
    
class CanCreateEventForSignedContract(permissions.BasePermission):
    def has_permission(self, request, view):
        contract_id = request.data.get('contract')
        if contract_id:
            contract = Contract.objects.filter(id=contract_id, is_signed=True).first()
            return contract and contract.client.sales_contact == request.user         
        
        return False
    
class IsCommercialUserAssigned(permissions.BasePermission):
    """Allow commercial users to create events for assigned clients with signed contracts."""
    def has_permission(self, request, view):
        if view.action == 'create':
            contract_id = request.data.get('contract')
            contract = get_object_or_404(Contract, pk=contract_id)
            return contract.is_signed and contract.client.sales_contact == request.user
        return True
    def has_object_permission(self, request, view, obj):
            return True  # Commercial users can view all events but not necessarily modify them
        
class IsSupportUserAssigned(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.contract.client.support_contact == request.user
    def has_object_permission(self, request, view, obj):
        return obj.support_contact == request.user if view.action in ['update', 'partial_update'] else True

class DenyDelete(permissions.BasePermission):
    """Deny delete permission to all users."""
    def has_object_permission(self, request, view, obj):
        return view.action != 'destroy'

class IsCommercial(permissions.BasePermission):
    def has_permission(self, request, view):        
        return request.user.is_authenticated and request.user.role == 'commercial'and view.action == 'create'

    def has_object_permission(self, request, view, obj):     
        return obj.contract.is_signed and obj.contract.sales_contact == request.user

class IsNotCommercial(permissions.BasePermission):
    message = 'Commercial users are not allowed to update events.'

    def has_permission(self, request, view):        
        return not (request.user.is_authenticated and request.user.role == 'commercial' and view.action in ['update', 'partial_update'])



class IsManagement(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'management'

    def has_object_permission(self, request, view, obj):        
        return request.method in permissions.SAFE_METHODS or request.method == 'PUT'

class IsSupport(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'support'

    def has_object_permission(self, request, view, obj):        
        return obj.support_contact == request.user