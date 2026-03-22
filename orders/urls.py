from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_history, name='order_history'),
]