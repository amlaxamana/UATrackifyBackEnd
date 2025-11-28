from django.shortcuts import render

# Create your views here.
from . models import FormRegistration, User, Organization
from . serializers import FormRegistrationSerializer, UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes

@api_view(['POST'])
def register_event(request):
    serializer = FormRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_events(request):
    events = FormRegistration.objects.all()
    serializer = FormRegistrationSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_dashboard(request):
    user = request.user
    
    # 🌟 CRITICAL CHECK: Ensure user is linked to an organization before proceeding
    if not user.organization:
        # Return a specific error instead of crashing with 500
        return Response({"error": "User profile must have an organization linked."}, 
                        status=status.HTTP_400_BAD_REQUEST) 
    
    # ... rest of your code ...

    # POST Logic:
    if request.method == 'POST':
        serializer = FormRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Pass the validated Organization object to the save method
            serializer.save(organization=user.organization)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # ...

    # GET Logic:
    elif request.method == 'GET':
        # Now this filter is safe because we checked user.organization is not None
        events = FormRegistration.objects.filter(OrganizationName=user.organization).order_by('-event_date')
        # ...

class EmailAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=400)

        user = authenticate(username=user.username, password=password)

        if not user:
            return Response({"error": "Invalid email or password"}, status=400)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        })
    