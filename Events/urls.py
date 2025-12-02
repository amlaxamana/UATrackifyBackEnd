from django.urls import path, include
from . import views
from .views import EmailAuthToken
from django.views.decorators.csrf import csrf_exempt
urlpatterns =[
    path('api/Events/' ,views.register_event, name='register_event'),
    path('api/Users/' ,views.register_user, name='register_user'),
    path('api/list_Users/' ,views.list_users, name='list_users'),
    path('api/list_Events/' ,views.list_events, name='list_events'),
    path('api/list_Organizations/', views.list_organizations, name='list_organizations'),
    path('api/Users/<int:pk>/', views.user_detail, name='user_detail'),
    path('api/Events/<int:pk>/', views.edit_form, name='event_detail'),
    path('api/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('auth/token/login/', csrf_exempt(EmailAuthToken.as_view()), name='api_token_auth'),
    path('api/download/<str:file_name>/', views.download_file, name='download_file'),
]
