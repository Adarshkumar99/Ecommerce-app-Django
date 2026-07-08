from ..models import Cart, CartItem
from products.models import Product, Category

"""
Central cart logic shared by cart/views.py, checkout/views.py,
products/views.py and accounts/views.py.

The cart supports two storage backends transparently:
  - Authenticated users: persisted in the Cart/CartItem models.
  - Guests: kept in the Django session as {product_id: quantity}.

Every helper below picks the right backend based on request.user, so
callers don't need to know or care whether the visitor is logged in.
"""


def get_user(request):
    """Safe accessor for request.user (guards against requests without an AuthenticationMiddleware-attached user)."""
    return getattr(request, "user", None)


def get_or_create_cart(request):
    """Returns the authenticated user's Cart, creating it on first use. Returns None for guests."""
    user = get_user(request)
    if user and user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart
    return None


def add_item(request, product_id):
    """
    Adds one unit of `product_id` to the cart.

    - Logged-in users: increments the matching CartItem's quantity (or
      creates a new CartItem at quantity 1).
    - Guests: increments the count in the session-backed cart dict.
    """
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
    """
    Removes one unit of `product_id` from the cart. If the resulting
    quantity would drop to zero, the line item is deleted entirely
    rather than left at quantity 0.
    """
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
    """
    Resolves the raw cart (model rows or session dict) into a list of
    dicts ready for template rendering, each containing the actual
    Product object, quantity and computed line total. Also returns the
    cart's grand total. Used by the cart page and by checkout to build
    the Stripe line items.
    """
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
    """
    Returns just the product IDs currently in the cart (as strings).
    Used by product list/detail pages to show an "already in cart"
    state on the Add to Cart button without pulling full cart details.
    """
    user = get_user(request)
    if user and user.is_authenticated:
        cart = get_or_create_cart(request)
        items = CartItem.objects.filter(cart=cart)
        return [str(item.product_id) for item in items]

    return list(request.session.get('cart', {}).keys())


def merge_cart(request):
    """
    Folds a guest's session cart into their persistent user Cart.

    Called right after login/registration (see accounts/views.py and
    cart/signals.py) so that items added before signing in aren't lost.
    Existing quantities in the user's cart are added to (not replaced
    by) the session quantities, then the session cart is cleared.
    """
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

                # Clear the session cart now that it's been merged in.
                request.session['cart'] = {}
