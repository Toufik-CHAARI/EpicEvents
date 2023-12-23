from rest_framework import serializers
from .models import Client, Contract, Event
from .models import CustomUser

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
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
        
        if not contract.is_signed:
            raise serializers.ValidationError("The contract is not signed.")
        
        
        
        # Allow management users to bypass the sales_contact check
        if user.role != 'management':
            if contract.client.sales_contact != user:
                raise serializers.ValidationError("You are not assigned to this client.")

        return data
