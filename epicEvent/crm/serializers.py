from rest_framework import serializers
from .models import Client, Contract, Event
from .models import CustomUser

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Client model, handling all fields ('__all__')
    of the model.
    """
    class Meta:
        model = Client
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contract model, encompassing all fields
    ('__all__') of the model.
    """
    class Meta:
        model = Contract
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model with custom handling for the
    'support_contact' field,limited to users with
    a 'support' role. Includes validation logic to enforce 
    business rules such as checking for a signed contract
    and appropriate user roles('management', 'support', 'commercial')
    in relation to event handling.
    """
    support_contact = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='support'), 
        required=False, allow_null=True
    )
    class Meta:
        model = Event
        fields = '__all__'
        
    def validate(self, data):
        user = self.context['request'].user
        contract = data.get('contract')
        event = self.instance         
    
        if contract and not contract.is_signed:
            raise serializers.ValidationError("The contract is not signed.")       
        
        if user.role == 'management':
            return data
        
        if user.role == 'support' and event and event.support_contact == user:
            return data
        
        if user.role == 'commercial' and contract.client.sales_contact != user:
            raise serializers.ValidationError("You are not assigned to this client.")

        return data
