from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('send_booking_request/', views.send_booking_request, name='send_booking_request'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-of-service/', views.terms_of_service, name='terms-of-service'),
]

