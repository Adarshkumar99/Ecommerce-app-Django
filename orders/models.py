from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
  """
  A single checkout attempt/purchase.

  Created as 'pending' the moment a Stripe Checkout Session is
  started (see checkout/views.py -> create_checkout_session), and
  flipped to 'success' only after Stripe's webhook confirms payment
  actually went through. `stripe_session_id` is how the webhook finds
  the right Order to update.
  """

  STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
  )

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  total_amount = models.FloatField()
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
  stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
  """
  A single product line within an Order.

  Stores a snapshot of the product's name and price at purchase time
  (rather than a live ForeignKey to Product) so the order history
  stays accurate even if the product is later renamed, repriced, or
  removed from the catalog.
  """

  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product_name = models.CharField(max_length=255)
  price = models.FloatField()
  quantity = models.IntegerField()

  def __str__(self):
    return self.product_name
