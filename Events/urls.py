from django.urls import path, include
from . import views

urlpatterns =[
    path('api/Events/' ,views.register_event, name='register_event'),
    path('api/Users/' ,views.register_user, name='register_user'),
    path('api/list_Users/' ,views.list_users, name='list_users'),
    path('api/list_Events/' ,views.list_events, name='list_events'),
    path('api/Users/<int:pk>/', views.user_detail, name='user_detail'),

]