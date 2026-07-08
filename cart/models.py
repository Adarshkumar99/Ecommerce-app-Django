from django.contrib.auth.models import User
from django.db import models


class Cart(models.Model):
    """
    A logged-in user's persistent shopping cart.

    Only created for authenticated users (see cart/helper/cart_util.py
    -> get_or_create_cart). Guests use the session instead, see
    `merge_cart()` for how the two are reconciled on login.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    """A single product line inside a user's Cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    # Stored as a plain integer FK (rather than models.ForeignKey to
    # Product) so cart items survive even if product lookups change;
    # resolved back to a Product instance on read via cart_util.
    product_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
