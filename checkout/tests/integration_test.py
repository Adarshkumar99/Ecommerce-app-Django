import pytest
from unittest.mock import patch, MagicMock
from django.urls import reverse
from orders.models import Order, OrderItem
from cart.models import Cart, CartItem

# ---- create_checkout_session ----
@pytest.mark.django_db
@patch('checkout.views.stripe.checkout.Session.create')
def test_create_checkout_session(mock_stripe, client, user, product, cart_with_item, user_password):
    mock_stripe.return_value = MagicMock(
        id='cs_test_fake123',
        url='https://checkout.stripe.com/test/fake123'
    )

    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })

    response = client.get(reverse('payment'))

    assert mock_stripe.called
    assert Order.objects.filter(user=user, status='pending').exists()
    assert response.status_code == 302
    assert response.url == 'https://checkout.stripe.com/test/fake123'


@pytest.mark.django_db
@patch('checkout.views.stripe.checkout.Session.create')
def test_order_items_saved(mock_stripe, client, user, product, cart_with_item, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    mock_stripe.return_value = MagicMock(
        id='cs_test_fake456',
        url='https://checkout.stripe.com/test/fake456'
    )

    client.get(reverse('payment'))

    order = Order.objects.get(user=user)
    assert OrderItem.objects.filter(order=order).exists()
    assert OrderItem.objects.get(order=order).product_name == product.name


@pytest.mark.django_db
@patch('checkout.views.stripe.checkout.Session.create')
def test_stripe_session_id_saved_in_order(mock_stripe, client, user, product, cart_with_item, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    mock_stripe.return_value = MagicMock(
        id='cs_test_session_id',
        url='https://checkout.stripe.com/test'
    )

    client.get(reverse('payment'))

    order = Order.objects.get(user=user)
    assert order.stripe_session_id == 'cs_test_session_id'


# ---- success ----
@pytest.mark.django_db
@patch('checkout.views.stripe.checkout.Session.retrieve')
def test_success_updates_order_status(mock_retrieve, user, client, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    mock_retrieve.return_value = MagicMock(
        payment_status='paid'
    )

    order = Order.objects.create(
        user=user,
        total_amount=200.00,
        status='pending',
        stripe_session_id='cs_test_123'
    )

    response = client.get(reverse('success'), {'session_id': 'cs_test_123'})

    order.refresh_from_db()
    assert order.status == 'success'
    assert response.status_code == 200


@pytest.mark.django_db
@patch('checkout.views.stripe.checkout.Session.retrieve')
def test_success_clears_cart(mock_retrieve, client, user, product, cart_with_item, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    mock_retrieve.return_value = MagicMock(
        payment_status='paid'
    )

    Order.objects.create(
        user=user,
        total_amount=200.00,
        status='pending',
        stripe_session_id='cs_test_123'
    )

    client.get(reverse('success'), {'session_id': 'cs_test_123'})

    assert not CartItem.objects.filter(cart=cart_with_item).exists()


@pytest.mark.django_db
@patch('checkout.views.stripe.checkout.Session.retrieve')
def test_success_page_loads_after_payment(mock_retrieve, client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    mock_retrieve.return_value = MagicMock(
        payment_status='paid'
    )

    Order.objects.create(
        user=user,
        total_amount=200.00,
        status='pending',
        stripe_session_id='cs_test_123'
    )

    response = client.get(reverse('success'), {'session_id': 'cs_test_123'})
    assert response.status_code == 200


@pytest.mark.django_db
@patch('checkout.views.stripe.checkout.Session.retrieve')
def test_success_unpaid_order_status_unchanged(mock_retrieve, client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    # payment status not paid
    mock_retrieve.return_value = MagicMock(
        payment_status='unpaid'
    )

    order = Order.objects.create(
        user=user,
        total_amount=200.00,
        status='pending',
        stripe_session_id='cs_test_unpaid'
    )

    client.get(reverse('success'), {'session_id': 'cs_test_unpaid'})

    order.refresh_from_db()
    assert order.status == 'pending' # no change