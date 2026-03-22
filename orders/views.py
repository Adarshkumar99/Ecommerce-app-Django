from django.shortcuts import render
from .models import Order

def order_history(request):
  orders = Order.objects.filter(user=request.user).order_by('-created_at')
  return render(request, 'order_history.html', {'orders': orders})