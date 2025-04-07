from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('devices/', views.device_list, name='device_list'),
    path('iot/viewdevice/<int:device_id>/', views.viewdevice, name='viewdevice'),
]
