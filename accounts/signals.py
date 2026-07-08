from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Auto-creates a Profile record whenever a new User is saved for the
    first time. Keeps Profile creation out of the view layer so it can
    never be forgotten, regardless of how the User was created
    (registration form, Django admin, shell, management command, etc.).
    """
    if created:
        Profile.objects.create(user=instance)
