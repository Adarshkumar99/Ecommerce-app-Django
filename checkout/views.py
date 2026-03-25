import stripe
from django.shortcuts import redirect, render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from cart.helper.cart_util import get_cart_data
from cart.models import Cart, CartItem
from .models import Address
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
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
                'unit_amount': int(item['product'].price * 100),
            },
            'quantity': item['quantity'],
        })
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

    order.stripe_session_id = session.id
    order.save()

    return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.payment_status == 'paid':
            try:
                order = Order.objects.get(stripe_session_id=session.id)
                order.status = 'success'
                order.save()

                cart = Cart.objects.filter(user=order.user).first()
                if cart:
                    CartItem.objects.filter(cart=cart).delete()
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)


def success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('home')
    return render(request, 'success.html')


def cancel(request):
    return render(request, 'cancel.html')