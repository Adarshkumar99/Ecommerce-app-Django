import pytest
from django.urls import reverse
from checkout.models import Address


@pytest.mark.django_db
def test_checkout_redirects_guest(client):
    response = client.get(reverse('checkout'))
    assert response.status_code == 302
    assert '/login' in response.url


@pytest.mark.django_db
def test_checkout_page_loads_logged_in(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    response = client.get(reverse('checkout'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_checkout_saves_address(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    client.post(reverse('checkout'), {
        'name': 'Test User',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'India',
        'pincode': '123456',
    })
    assert Address.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_checkout_address_correct_data(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    client.post(reverse('checkout'), {
        'name': 'Test User',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'India',
        'pincode': '123456',
    })
    address = Address.objects.get(user=user)
    assert address.full_name == 'Test User'
    assert address.phone == '1234567890'
    assert address.city == 'Test City'
    assert address.pincode == '123456'


@pytest.mark.django_db
def test_checkout_redirects_to_payment_after_address(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    response = client.post(reverse('checkout'), {
        'name': 'Test User',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'India',
        'pincode': '123456',
    })
    assert response.status_code == 302
    assert response.url == reverse('payment')


@pytest.mark.django_db
def test_checkout_address_linked_to_correct_user(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    client.post(reverse('checkout'), {
        'name': 'Test User',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'India',
        'pincode': '123456',
    })
    address = Address.objects.get(user=user)
    assert address.user == user


@pytest.mark.django_db
def test_multiple_addresses_per_user(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    client.post(reverse('checkout'), {
        'name': 'Test User',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'India',
        'pincode': '123456',
    })
    client.post(reverse('checkout'), {
        'name': 'Test User 2',
        'phone': '9876543210',
        'address': '456 Another Street',
        'city': 'Another City',
        'state': 'Test State',
        'country': 'India',
        'pincode': '654321',
    })
    assert Address.objects.filter(user=user).count() == 2


@pytest.mark.django_db
def test_cancel_page_loads(client):
    response = client.get(reverse('cancel'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_success_without_session_id_redirects(client, user, user_password):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    response = client.get(reverse('success'))
    assert response.status_code == 302
    assert response.url == '/'


@pytest.mark.django_db
def test_address_str(user):
    address = Address.objects.create(
        user=user,
        full_name='Test User',
        phone='1234567890',
        address_line='123 Test Street',
        city='Test City',
        state='Test State',
        country='India',
        pincode='123456',
    )
    assert str(address) == 'Test User'