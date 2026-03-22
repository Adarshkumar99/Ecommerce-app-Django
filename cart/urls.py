from django.urls import path, include
from . import views 


urlpatterns = [
  path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
  path('', views.cart_detail, name='cart_detail'),
  path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]   