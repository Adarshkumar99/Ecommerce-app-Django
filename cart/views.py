from django.shortcuts import render, redirect
from .helper.cart_util import add_item, get_cart_data, remove_item
from .models import Cart, CartItem

def add_to_cart(request, product_id):
    add_item(request, product_id)
    return redirect(request.META.get('HTTP_REFERER'))


def cart_detail(request):
    cart_items, total = get_cart_data(request)

    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'max_total_price': total
    })


def remove_from_cart(request, product_id):
    remove_item(request, product_id)
    return redirect('cart_detail')