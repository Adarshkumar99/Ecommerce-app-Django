from django.urls import path, include
from . import views

# Mounted at /products/ in Ecommerce/urls.py.
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
]
