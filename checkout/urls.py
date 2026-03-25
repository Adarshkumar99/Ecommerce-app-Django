from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('payment/', views.create_checkout_session, name='payment'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]