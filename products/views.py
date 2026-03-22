from django.shortcuts import render
from .models import Product, Category
from cart.helper.cart_util import get_cart_ids


def product_list(request):
    # Here we are checking if there is a category query parameter in the URL, if there is we filter the products by that category, otherwise we return all products
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
    product = Product.objects.get(pk=pk)
    cart_ids = get_cart_ids(request)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_ids': cart_ids
    })