from django.urls import path
from . import views

# Mounted at /orders/ in Ecommerce/urls.py.
urlpatterns = [
    path('', views.order_history, name='order_history'),
]
