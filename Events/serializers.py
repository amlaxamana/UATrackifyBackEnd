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
        read_only_fields = ['date_added'] 
        

class UserSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.all(),
        slug_field='OrganizationName',
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'office', 'organization'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def validate(self, data):
        role = data.get('role')
        organization = data.get('organization')
        office = data.get('office')

        if role == 'admin':
            if not office or office.strip() == "":
                raise serializers.ValidationError({'office': 'Office is required for admins.'})
            if organization:
                raise serializers.ValidationError({'organization': 'Admin cannot belong to an organization.'})

        elif role == 'student':
            if not organization:
                raise serializers.ValidationError({'organization': 'Organization is required for students.'})
            if office and office.strip() != "":
                raise serializers.ValidationError({'office': 'Students cannot have an office.'})
        return data

    def create(self, validated_data):
        organization_instance = validated_data.pop('organization', None)
        role = validated_data.get('role')

        # Always hash the password
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password

        # Set permissions
        if role == 'admin':
            validated_data['is_staff'] = True
            validated_data['is_superuser'] = True
            validated_data['is_active'] = True
        else:
            validated_data['is_staff'] = False
            validated_data['is_superuser'] = False
            validated_data['is_active'] = True

        user = super().create(validated_data)

        if organization_instance:
            user.organization = organization_instance
            user.save()

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)

        organization_instance = validated_data.pop('organization', None)
        if organization_instance is not None:
            instance.organization = organization_instance

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'OrganizationName']