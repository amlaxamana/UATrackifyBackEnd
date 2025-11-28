from rest_framework import serializers
from . models import FormRegistration, User, Organization
from django.contrib.auth.hashers import make_password


class FormRegistrationSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.all(),
        slug_field='OrganizationName'
    )
    
    class Meta:
        model = FormRegistration
        fields = '__all__'
        

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.all(),
        slug_field='OrganizationName',
        required=False, 
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'office', 'organization']
        extra_kwargs = {
            'email': {'required': True},
            'password': {'write_only': True},
            'office': {'required': False}, 
        }

    # 🎯 ADDED: Conditional Validation Logic
    def validate(self, data):
        role = data.get('role')
        organization = data.get('organization') # This is the object instance if lookup succeeded, or None/string if not.
        office = data.get('office') # This is the string value

        if role == 'admin':
            # 1. Enforce Office requirement for Admin (office field cannot be empty string or None)
            if not office or office.strip() == "":
                raise serializers.ValidationError({
                    'office': 'The office field is required for Administrator roles.'
                })
            
            # 2. Prevent Organization for Admin
            if organization:
                raise serializers.ValidationError({
                    'organization': 'Organization must be left empty for Administrator roles.'
                })

        elif role == 'student':
            # 1. Enforce Organization requirement for Student (organization must be provided)
            if not organization:
                raise serializers.ValidationError({
                    'organization': 'The organization field is required for Student roles.'
                })
            
            # 2. Prevent Office for Student
            if office and office.strip() != "":
                 raise serializers.ValidationError({
                    'office': 'Office must be left empty for Student roles.'
                })

        return data
    
    # Custom create method (left untouched as requested)
    def create(self, validated_data):
        # 💡 FIX 1: Extract the organization object before manipulating validated_data
        organization_instance = validated_data.pop('organization', None) 
        
        role = validated_data.get('role')
        if role == 'admin':
            validated_data['is_staff'] = True
            validated_data['is_superuser'] = True
            
        validated_data['password'] = make_password(validated_data['password'])
        
        # Create the user without the organization field initially
        user = super().create(validated_data) 
        
        # 💡 FIX 2: Manually set and save the organization object onto the user
        if organization_instance:
            user.organization = organization_instance
            user.save()
            
        return user