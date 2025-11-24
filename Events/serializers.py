from rest_framework import serializers
from . models import FormRegistration, User
from django.contrib.auth.hashers import make_password

class FormRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FormRegistration
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email', 'password', 'first_name', 'last_name', 'role', 'organization', 'office']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.get('role')
        if role == 'admin':
            validated_data['is_staff'] = True
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)