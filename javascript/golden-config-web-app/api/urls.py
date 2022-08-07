from django.urls import path
from .views import device_list, device_detail


urlpatterns = [
    path('api/', device_list, name="devices"),
    path('api/<int:pk>/', device_detail, name="device details"),
]