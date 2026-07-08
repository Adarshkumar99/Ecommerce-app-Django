from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
  """Product category used for catalog navigation and filtering (see products/views.py -> product_list)."""

  name = models.CharField(max_length=200)

  def __str__(self):
    return self.name


class Product(models.Model):
  """A single sellable item in the store."""

  name = models.CharField(max_length=255)
  # Rich text editor (CKEditor) field so descriptions can include
  # formatting, links, images, etc. from the Django admin.
  description = RichTextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
  stock = models.PositiveIntegerField()
  # Uploaded to local MEDIA_ROOT in development; served from Cloudinary
  # in production when USE_CLOUDINARY=True (see Ecommerce/settings.py).
  image = models.ImageField(upload_to="product_images/", null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name
