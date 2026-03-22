from django.shortcuts import render, redirect
from products.models import Product, Category
from cart.models import Cart, CartItem


# Create your views here.

def home(request):
  products = Product.objects.all()[:10] #display first 10 products
  categories = Category.objects.all() # loads all the category objects
  return render(request, 'core/home.html', {'products': products, 'categories': categories })

def contact(request):
  return render(request, 'core/contact.html')

def about(request):
  return render(request, 'core/about.html')
