from django.contrib.auth.models import User
from django.db import models

class Address(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  full_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=15)
  address_line = models.TextField()
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  country = models.CharField(max_length=50)
  pincode = models.CharField(max_length=10)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.full_name