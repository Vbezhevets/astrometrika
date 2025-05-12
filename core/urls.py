from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('send_booking_request/', views.send_booking_request, name='send_booking_request'),
]
