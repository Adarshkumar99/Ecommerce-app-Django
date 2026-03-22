from django.contrib import admin
from .models import Product, Category


admin.site.site_header = "LifeStore Admin"
admin.site.site_title = "LifeStore Admin Portal"
admin.site.index_title = "Welcome to LifeStore Admin Portal"
admin.site.register(Product)
admin.site.register(Category)
