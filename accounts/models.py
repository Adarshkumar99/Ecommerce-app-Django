from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Extends Django's built-in User model with e-commerce-specific fields.

    A Profile is automatically created for every new User via the
    `create_profile` signal handler in accounts/signals.py.
    """

    # One-to-one link to Django's auth User. Deleting the user cascades
    # and removes the profile as well.
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Flips to True once the user clicks the email verification link
    # sent during registration (see accounts/views.py -> verify_email).
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
