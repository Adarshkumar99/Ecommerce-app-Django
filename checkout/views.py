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
    """
    Step 1 of checkout: collect a shipping address.

    Requires login. On POST, saves the submitted address for the
    current user and moves on to the Stripe payment step.
    """
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
    """
    Step 2 of checkout: build a Stripe Checkout Session from the
    current cart and redirect the user to Stripe's hosted payment page.

    An Order is created up front with status='pending' (and the
    matching OrderItem rows), then linked to the Stripe session via
    `stripe_session_id` so the webhook can find it later and mark it
    paid once Stripe confirms payment.
    """
    cart_items, total = get_cart_data(request)
    line_items = []
    domain = request.scheme + "://" + request.get_host()

    order = Order.objects.create(
        user=request.user,
        total_amount=total,
        status='pending'
    )

    for item in cart_items:
        # Stripe expects amounts in the smallest currency unit (cents),
        # hence the `* 100`.
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
        # Snapshot the product name/price at time of purchase so the
        # order record stays accurate even if the product is later
        # renamed, repriced, or deleted.
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
    """
    Receives asynchronous payment confirmation events directly from
    Stripe's servers (not the user's browser), so it's CSRF-exempt and
    instead verified using Stripe's own signature check
    (`STRIPE_WEBHOOK_SECRET`). This is the source of truth for whether
    a payment actually succeeded -- the success_url redirect alone
    cannot be trusted, since a user could hit it without actually paying.

    On a confirmed `checkout.session.completed` + paid event:
      - marks the matching Order as 'success'
      - empties the user's persisted cart
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload.
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Signature didn't match -- request didn't actually come from Stripe.
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        if session.payment_status == 'paid':
            try:
                order = Order.objects.get(stripe_session_id=session.id)
                order.status = 'success'
                order.save()

                # Payment confirmed -- safe to empty the cart now.
                cart = Cart.objects.filter(user=order.user).first()
                if cart:
                    CartItem.objects.filter(cart=cart).delete()
            except Order.DoesNotExist:
                pass

    # Always return 200 once handled, otherwise Stripe will keep retrying.
    return HttpResponse(status=200)


def success(request):
    """
    Landing page after a successful Stripe redirect. Note: this page
    alone does NOT confirm payment -- that's the webhook's job -- it's
    purely a user-facing "thank you" screen.
    """
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('home')
    return render(request, 'success.html')


def cancel(request):
    """Landing page shown if the user backs out of the Stripe payment page."""
    return render(request, 'cancel.html')
