import stripe
from django.shortcuts import redirect, render
from django.conf import settings
from cart.helper.cart_util import get_cart_data
from cart.models import Cart, CartItem
from .models import Address
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
  if not request.user.is_authenticated:
    return redirect('login')

  if request.method == 'POST':
    # save address
    Address.objects.create(
      user=request.user,
      full_name=request.POST.get('name'),
      phone=request.POST.get('phone'),
      address_line=request.POST.get('address'),
      city=request.POST.get('city'),
      state=request.POST.get('state'),
      country=request.POST.get('country'),
      pincode=request.POST.get('pincode'),
    )

    return redirect('payment')

  return render(request, 'checkout/address.html')



def create_checkout_session(request):
    cart_items, total = get_cart_data(request)

    line_items = []
    domain = request.scheme + "://" + request.get_host()
    # Create order in database with status 'pending'
    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status='pending'
    )

    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['product'].name,
                },
                'unit_amount': int(item['product'].price * 100),  # cents
            },
            'quantity': item['quantity'],
        })
        # Save order item to database
        OrderItem.objects.create(
            order=order,
            product_name=item['product'].name,
            price=item['product'].price,
            quantity=item['quantity']
        )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=f"{domain}/checkout/success/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=request.build_absolute_uri('/checkout/cancel'),
    )

    # Update order with Stripe session ID
    order.stripe_session_id = session.id
    order.save()

    return redirect(session.url)


def success(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return redirect('home')

    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        # Update order status to 'success'
        try:
            order = Order.objects.get(stripe_session_id=session_id)
            order.status = 'success'
            order.save()
        except Order.DoesNotExist:
            pass
        
        # cart clear
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                CartItem.objects.filter(cart=cart).delete()
            except Cart.DoesNotExist:
                pass
        else:
            request.session['cart'] = {}

    return render(request, 'success.html')


def cancel(request):
    # Logic to handle canceled payment
    # Update order status to 'canceled'
    session_id = request.GET.get('session_id')
    if session_id:
      try:
        order = Order.objects.get(stripe_session_id=session_id).first()
        order.status = 'failed'
        order.save()
      except Order.DoesNotExist:
        pass
      
    return render(request, 'cancel.html')
