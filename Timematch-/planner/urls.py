from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/create-event/', views.create_event, name='create_event'),
    path('dashboard/join-event/', views.join_event, name='join_event'),
    path('dashboard/availability-input/', views.availability_input, name='availability_input'),
    path('dashboard/event-overview/', views.event_overview, name='event_overview'),
    path('dashboard/notification-panel/', views.notification_panel, name='notification_panel'),
]