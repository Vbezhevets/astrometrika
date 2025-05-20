from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),

    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('terms-of-service/', views.terms_of_service, name='terms-of-service'),
    path('test-mail/', views.test_mail),

    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success_page, name='payment-success'),
    path('cancel/', views.cancel_page, name='payment-cancel'),

]


