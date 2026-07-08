from django.shortcuts import render
from .models import Order


def order_history(request):
  """Displays the logged-in user's past orders, most recent first."""
  orders = Order.objects.filter(user=request.user).order_by('-created_at')
  return render(request, 'order_history.html', {'orders': orders})
