from .models import Cart, CartItem

def cart_item_count(request):
  if request.user.is_authenticated:
    try:
      cart = Cart.objects.get(user=request.user)
      count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
    except Cart.DoesNotExist:
      count = 0
  else:
    cart = request.session.get('cart', {})
    count = sum(cart.values())

  return {
    'cart_item_count': count
  }