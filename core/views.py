from django.shortcuts import render, redirect
from products.models import Product, Category
from cart.models import Cart, CartItem


def home(request):
  """Landing page: shows a preview of the first 10 products plus all categories for site navigation."""
  products = Product.objects.all()[:10]  # display first 10 products
  categories = Category.objects.all()  # loads all the category objects
  return render(request, 'core/home.html', {'products': products, 'categories': categories})


def contact(request):
  """Static contact page."""
  return render(request, 'core/contact.html')


def about(request):
  """Static about page."""
  return render(request, 'core/about.html')
