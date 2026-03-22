import pytest
from django.urls import reverse
from cart.models import Cart, CartItem
from products.models import Product, Category
from cart.helper.cart_util import get_or_create_cart, add_item, remove_item, merge_cart
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

# ========================
# UNIT TESTS — cart_util
# ========================

@pytest.mark.django_db
def test_get_or_create_cart_logged_in(user):

    request = request_user(user)

    cart = get_or_create_cart(request)
    assert cart is not None
    assert cart.user == user


@pytest.mark.django_db
def test_get_or_create_cart_guest():

    request = anonymous_user()

    cart = get_or_create_cart(request)
    assert cart is None


@pytest.mark.django_db
def test_add_item_logged_in_user(user, product):
    request = request_user(user)
    request.session = {}

    add_item(request, product.id)

    cart = Cart.objects.get(user=user)
    assert CartItem.objects.filter(cart=cart, product_id=product.id).exists()


@pytest.mark.django_db
def test_add_item_increases_quantity(user, product):

    request = request_user(user)
    request.session = {}

    add_item(request, product.id)
    add_item(request, product.id)

    cart = Cart.objects.get(user=user)
    item = CartItem.objects.get(cart=cart, product_id=product.id)
    assert item.quantity == 2


@pytest.mark.django_db
def test_add_item_guest_session():

    request = anonymous_user()
    request.session = {}

    add_item(request, 1)
    assert request.session['cart']['1'] == 1

    add_item(request, 1)
    assert request.session['cart']['1'] == 2


@pytest.mark.django_db
def test_remove_item_logged_in(user, product):

    request = request_user(user)
    request.session = {}

    add_item(request, product.id)
    add_item(request, product.id)  # quantity = 2
    remove_item(request, product.id)  # quantity = 1

    cart = Cart.objects.get(user=user)
    item = CartItem.objects.get(cart=cart, product_id=product.id)
    assert item.quantity == 1


@pytest.mark.django_db
def test_remove_item_deletes_when_quantity_one(user, product):

    request = request_user(user)
    request.session = {}

    add_item(request, product.id)   # quantity = 1
    remove_item(request, product.id)  # delete

    cart = Cart.objects.get(user=user)
    assert not CartItem.objects.filter(cart=cart, product_id=product.id).exists()


@pytest.mark.django_db
def test_merge_cart(user, product):
    request = request_user(user)
    request.session = {'cart': {str(product.id): 3}}  # 3 items in session

    merge_cart(request)

    cart = Cart.objects.get(user=user)
    item = CartItem.objects.get(cart=cart, product_id=product.id)
    assert item.quantity == 3
    assert request.session['cart'] == {}  # clear the session


def request_user(user):
  factory = RequestFactory()
  request = factory.get('/')
  request.user = user
  return request

def anonymous_user():
  factory = RequestFactory()
  request = factory.get('/')
  request.user = AnonymousUser()
  return request
