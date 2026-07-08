from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .helper.cart_util import merge_cart


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """
    Whenever ANY login happens (including via Django admin, not just
    our custom login view), fold the guest's session cart into their
    persistent user Cart. Keeping this on the `user_logged_in` signal
    (rather than only inside accounts/views.py) guarantees the merge
    can never be skipped, regardless of which code path logs the user in.
    """
    merge_cart(request)
