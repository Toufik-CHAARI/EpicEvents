from rest_framework import generics,permissions
from crm.models import Contract
from crm.serializers import ContractSerializer
from django.shortcuts import get_object_or_404

class ManagementOnlyAccess(permissions.BasePermission):
    """
    Custom permission that grants full access rights
    exclusively to management users. It checks if the user
    is authenticated and has a role of 'management'.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'management'

class IsCommercialUser(permissions.BasePermission):
    """
    Custom permission that defines access rights for commercial 
    users.It checks permissions based on user's role and specific
    action performed in the view. It restricts actions like create,
    update,and partial update to commercial users and has additional
    object-level permission checks based on the sales contact or
    client's sales contact associated . It also includes a method
    that verifies if a commercial user can create an event, ensuring
    that the associated contract is signed.
    """
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
        contract_id = request.data.get('contract')
        if contract_id:
            try:
                contract = Contract.objects.get(id=contract_id, is_signed=True)
                return contract.client.sales_contact == request.user
            except Contract.DoesNotExist:
                return False
        return False
    

class ManagementOrSuperuserAccess(permissions.BasePermission):
    """
    Custom permission class which allows access to users with
    management or superusers access rights. It checks if user
    is authenticated and then verifies if the assotiated role is
    'superuser' or 'management'.it is used for scenarios
    where both management and superusers require similar access rights.
    """
    def has_permission(self, request, view):
        
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'management'
        )
        
class IsSupportUser(permissions.BasePermission):
    """
    Custom permission for support users. It allows access
    if the user is authenticated and has a role of 'support'.
    It also includes object-level permission checks, granting
    'update' and 'partial_update' permissions only if the user
    is the support contact associated with the object. 
    """
    def has_permission(self, request, view):
        
        return request.user.is_authenticated and request.user.role == 'support'

    def has_object_permission(self, request, view, obj):
        
        return obj.support_contact == request.user if view.action in ['update', 'partial_update'] else True
    
class IsCommercialUserCont(permissions.BasePermission):
    """
    Custom permission class for commercial users.It denies 'create'
    action and it checks if the user is authenticated and has a
    role of 'commercial'. For object-level permissions,
    it grants 'update' and 'partial_update' permissions only if
    the user is the sales contact associated with the object. 
    For other actions, permission is granted by default.
    """
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
    Custom permission that denies access to all users. 
    Both class-level and object-level permissions
    return False, ensuring no user is 
    granted access regardless of their authentication
    status or role.
    """
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False

class IsCommercial(permissions.BasePermission):
    """
    Custom permission class for commercial users which
    grants permission only if the user is authenticated,
    has a role of 'commercial', and is performing
    the 'create' action. For object-level permissions,
    it checks whether the contract associated is signed 
    and if the user is the sales contact for that contract.   
    """
    def has_permission(self, request, view):        
        return request.user.is_authenticated and request.user.role == 'commercial'and view.action == 'create'

    def has_object_permission(self, request, view, obj):     
        return obj.contract.is_signed and obj.contract.sales_contact == request.user

class IsNotCommercial(permissions.BasePermission):
    
    """
    Custom permission class which prevents commercial users
    from updating events.It denies permission if the user
    is authenticated, has a role of 'commercial', and is
    attempting to perform 'update' or 'partial_update'
    actions.This includes a custom message 
    explaining that commercial users are not
    allowed to update events, enhancing user feedback 
    when access is denied.
    """
    
    message = 'Commercial users are not allowed to update events.'

    def has_permission(self, request, view):        
        return not (request.user.is_authenticated and request.user.role == 'commercial' and view.action in ['update', 'partial_update'])

class IsManagement(permissions.BasePermission):
    """
    Custom permission for users with a 'management' role. 
    It grants access if the user is authenticated and has
    a 'management' role.The object-level permissions allow
    access for safe HTTP methods(e.g., GET, HEAD, OPTIONS)
    as well as PUT and PATCH methods. This setup enables
    management users to both view and modify data, but
    with restrictions on the modification methods they can use.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'management'

    def has_object_permission(self, request, view, obj):        
        
        return (
            request.method in permissions.SAFE_METHODS or
            request.method in ['PUT', 'PATCH']
        )

class IsSupport(permissions.BasePermission):
    """
    Custom permission for users with a 'support' role. 
    It allows access to those who are authenticated and
    have a role of 'support'.At the object level, permissions
    are granted if the user is the support contact associated 
    with the object in question. 
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'support'

    def has_object_permission(self, request, view, obj):        
        return obj.support_contact == request.user
    
    
    
