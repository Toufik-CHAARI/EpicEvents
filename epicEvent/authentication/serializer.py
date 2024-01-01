from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    """
    This serializer for the CustomUser model handles the serialization
    and deserialization of CustomUser objects,it allows for operations
    like creating and updating user instances.   

    The 'create' method is overridden to use the 'create_user' method
    of the CustomUser model, ensuring that user instances are
    correctly created with all necessary attributes, including 
    setting and hashing the password.
    The 'update' method is also overridden to allow updating the user
    instance with new data.It updates fields if provided in
    'validated_data', and specifically handles password changes 
    by setting and saving a new hashed password if a new one is
    provided.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email','role', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
