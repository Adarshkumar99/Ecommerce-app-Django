import pytest
from django.contrib.auth.models import User
from django.urls import reverse

# ---- REGISTER TESTS ----
@pytest.mark.django_db
def test_register_page_loads(client):
    response = client.get(reverse('register'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_register_valid_user(client):
    response = client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'test@test.com',
        'first_name': 'Test',
        'last_name': 'User', 
        'password1': 'StrongPass123!',
        'password2': 'StrongPass123!',
    })
    assert User.objects.filter(username='testuser').exists()
    assert response.status_code == 302  # redirect hona chahiye

@pytest.mark.django_db
def test_register_password_mismatch(client):
    client.post(reverse('register'), {
        'username': 'testuser',
        'email': 'test@test.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password1': 'StrongPass123!',
        'password2': 'WrongPass123!',
    })
    assert not User.objects.filter(username='testuser').exists()

@pytest.mark.django_db
def test_register_duplicate_username(client, user):
    response = client.post(reverse('register'), {
        'username': user.username,  # fixture from conftest.py
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'password1': user.password,  # using the same password for simplicity
        'password2': user.password,
    })
    assert User.objects.filter(username='testuser').count() == 1


# ---- LOGIN TESTS ----
@pytest.mark.django_db
def test_login_page_loads(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_valid_credentials(client, user, user_password):
    response = client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    assert response.status_code == 302

@pytest.mark.django_db
def test_login_invalid_credentials(client, user):
    response = client.post(reverse('login'), {
        'username': user.username,
        'password': 'WrongPassword!',
    })
    assert response.status_code == 200

@pytest.mark.django_db
def test_login_nonexistent_user(client):
    response = client.post(reverse('login'), {
        'username': 'ghostuser',
        'password': 'StrongPass123!',
    })
    assert response.status_code == 200

# ---- LOGOUT TESTS ----

@pytest.mark.django_db
def test_logout(client, user, user_password):
    client.login(username=user.username, password=user_password)
    response = client.get(reverse('logout'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_logout_actually_logs_out(client, user, user_password):
    client.login(username=user.username, password=user_password)
    client.get(reverse('logout'))
    # after logout, trying to access a protected page should redirect to login
    response = client.get(reverse('register'))
    assert response.status_code == 200