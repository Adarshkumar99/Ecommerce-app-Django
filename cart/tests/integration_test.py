import pytest
from django.urls import reverse
from cart.models import Cart, CartItem
from products.models import Product, Category

# ========================
# INTEGRATION TESTS — views
# ========================

@pytest.mark.django_db
def test_add_to_cart_logged_in(client, user, user_password, product):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    client.get(
      reverse('add_to_cart', args=[product.id]),
      HTTP_REFERER=reverse('product_list'))

    cart = Cart.objects.get(user=user)
    assert CartItem.objects.filter(cart=cart, product_id=product.id).exists()


@pytest.mark.django_db
def test_add_to_cart_guest(client, product):
    client.get(reverse('add_to_cart', args=[product.id]),
    HTTP_REFERER=reverse('product_list'))

    session = client.session
    assert str(product.id) in session.get('cart', {})


@pytest.mark.django_db
def test_cart_detail_page_loads(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    response = client.get(reverse('cart_detail'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_remove_from_cart(client, user, user_password, product):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })

    # add
    client.get(reverse('add_to_cart', args=[product.id]),
    HTTP_REFERER=reverse('product_list'))

    # remove
    client.get(reverse('remove_from_cart', args=[product.id]),
    HTTP_REFERER=reverse('cart_detail'))

    cart = Cart.objects.get(user=user)
    assert not CartItem.objects.filter(cart=cart, product_id=product.id).exists()


@pytest.mark.django_db
def test_cart_detail_shows_items(client, user, user_password, product):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    client.get(reverse('add_to_cart', args=[product.id]),
    HTTP_REFERER=reverse('product_list'))

    response = client.get(reverse('cart_detail'))
    assert response.status_code == 200
    assert 'cart_items' in response.context
    assert len(response.context['cart_items']) == 1