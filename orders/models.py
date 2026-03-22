from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
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
  order = models.ForeignKey(Order, on_delete=models.CASCADE)
  product_name = models.CharField(max_length=255)
  price = models.FloatField()
  quantity = models.IntegerField()

  def __str__(self):
    return self.product_name