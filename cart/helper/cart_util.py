from ..models import Cart, CartItem
from products.models import Product, Category


def get_user(request):
  return getattr(request, "user", None)

def get_or_create_cart(request):
  user = get_user(request)
  if user and user.is_authenticated:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart
  return None


def add_item(request, product_id):
  user = get_user(request)
  if user and user.is_authenticated:
    cart = get_or_create_cart(request)

    item, created = CartItem.objects.get_or_create(
      cart=cart,
      product_id=product_id
    )

    if not created:
      item.quantity += 1
      item.save()

  else:
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
      cart[str(product_id)] += 1
    else:
      cart[str(product_id)] = 1

    request.session['cart'] = cart


def remove_item(request, product_id):
  user = get_user(request)
  if user and user.is_authenticated:
    try:
      cart = get_or_create_cart(request)
      item = CartItem.objects.get(cart=cart, product_id=product_id)

      if item.quantity > 1:
        item.quantity -= 1
        item.save()
      else:
        item.delete()

    except CartItem.DoesNotExist:
      pass

  else:
    cart = request.session.get('cart', {})
    quantity = cart.get(str(product_id), 0)

    if quantity > 1:
      cart[str(product_id)] -= 1
    elif str(product_id) in cart:
      del cart[str(product_id)]

    request.session['cart'] = cart


def get_cart_data(request):
  cart_items = []
  total = 0

  if request.user.is_authenticated:
    cart = get_or_create_cart(request)
    items = CartItem.objects.filter(cart=cart)

    for item in items:
      product = Product.objects.get(id=item.product_id)
      total_price = product.price * item.quantity

      total += total_price
      cart_items.append({
        'product': product,
        'quantity': item.quantity,
        'total_price': total_price
      })

  else:
    cart = request.session.get('cart', {})

    for product_id, quantity in cart.items():
      product = Product.objects.get(id=product_id)
      total_price = product.price * quantity

      total += total_price
      cart_items.append({
        'product': product,
        'quantity': quantity,
        'total_price': total_price
      })

  return cart_items, total


def get_cart_ids(request):
  user = get_user(request)
  if user and user.is_authenticated:
    cart = get_or_create_cart(request)
    items = CartItem.objects.filter(cart=cart)
    return [str(item.product_id) for item in items]

  return list(request.session.get('cart', {}).keys())

def merge_cart(request):
  user = get_user(request)
  if user and user.is_authenticated:
    session_cart = request.session.get('cart', {})

    if session_cart:
      cart = get_or_create_cart(request)

      for product_id, quantity in session_cart.items():
        item, created = CartItem.objects.get_or_create(
          cart=cart,
          product_id=product_id
        )

        if not created:
          item.quantity += quantity
        else:
          item.quantity = quantity

        item.save()

        # session clear
        request.session['cart'] = {}