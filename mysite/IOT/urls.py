from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.device_list, name='device_list'),
    path('device/<int:device_id>/', views.viewdevice, name='viewdevice'),
]
