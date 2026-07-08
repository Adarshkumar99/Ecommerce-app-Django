from .models import Cart, CartItem


def cart_item_count(request):
    """
    Template context processor that exposes `cart_item_count` in every
    template's context (registered in Ecommerce/settings.py under
    TEMPLATES -> OPTIONS -> context_processors).

    This powers the cart badge/icon shown in the site header on every
    page, without every view having to compute and pass it manually.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
        except Cart.DoesNotExist:
            count = 0
    else:
        # Guests: cart lives in the session as {product_id: quantity}.
        cart = request.session.get('cart', {})
        count = sum(cart.values())

    return {
        'cart_item_count': count
    }
