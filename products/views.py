from django.shortcuts import render
from .models import Product, Category
from cart.helper.cart_util import get_cart_ids


def product_list(request):
    """
    Displays the product catalog. Supports an optional `?category=`
    query param to filter by category name (case-insensitive); shows
    all products otherwise.

    Also passes `cart_ids` so the template can render an "in cart"
    state on each product card without a separate lookup per item.
    """
    categories = request.GET.get('category')
    if categories:
        products = Product.objects.filter(category__name__iexact=categories)
    else:
      products = Product.objects.all()

    cart_ids = get_cart_ids(request)
    return render(request, 'products/product_list.html', {
        'products': products,
        'cart_ids': cart_ids
    })


def product_detail(request, pk):
    """Displays a single product's detail page, including its current cart status."""
    product = Product.objects.get(pk=pk)
    cart_ids = get_cart_ids(request)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_ids': cart_ids
    })
