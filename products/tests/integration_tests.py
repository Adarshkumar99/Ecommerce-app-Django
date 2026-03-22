import pytest
from django.urls import reverse
from products.models import Product, Category


# ---- product list ----

@pytest.mark.django_db
def test_product_list_page_loads(client):
    response = client.get(reverse('product_list'))
    assert response.status_code == 200

@pytest.mark.django_db
def test_product_list_shows_products(client, product):
    response = client.get(reverse('product_list'))
    assert product in response.context['products']

@pytest.mark.django_db
def test_product_list_filter_by_category(client, product, category2):
    response = client.get(reverse('product_list'), {'category': 'Mobile'})
    assert product in response.context['products']

@pytest.mark.django_db
def test_product_list_filter_wrong_category(client, product):
    response = client.get(reverse('product_list'), {'category': 'wrongcategory'})
    assert product not in response.context['products']

@pytest.mark.django_db
def test_product_list_no_category_filter(client, product):
    response = client.get(reverse('product_list'))
    assert len(response.context['products']) >= 1

@pytest.mark.django_db
def test_product_list_case_insensitive_filter(client, product, category2):
    # iexact test — MOBILE, Mobile, Mobiles all working
    response = client.get(reverse('product_list'), {'category': 'mobile'})
    assert product in response.context['products']


# ---- product detail ----

@pytest.mark.django_db
def test_product_detail_page_loads(client, product):
    response = client.get(reverse('product_detail', args=[product.id]))
    assert response.status_code == 200

@pytest.mark.django_db
def test_product_detail_shows_correct_product(client, product):
    response = client.get(reverse('product_detail', args=[product.id]))
    assert response.context['product'] == product

@pytest.mark.django_db
def test_product_detail_has_cart_ids(client, user, user_password, product):
    client.post(reverse('login'), {
        'username': user.username,
        'password': user_password,
    })
    response = client.get(reverse('product_detail', args=[product.id]))
    assert 'cart_ids' in response.context