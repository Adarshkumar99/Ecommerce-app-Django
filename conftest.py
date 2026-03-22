import pytest
from django.contrib.auth.models import User
from products.models import Product, Category
from cart.models import Cart, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def hello():
    return "hello"

@pytest.fixture
def user_password():
    return 'StrongPass123!'

@pytest.fixture
def user(db, user_password):
  return User.objects.create_user(
    username = 'testuser',
    first_name = 'Test',
    last_name = 'User', 
    email = 'test@test.com',
    password = user_password
  )


@pytest.fixture
def logged_in_client(client, user):
  client.login(username='testuser', password='StrongPass123!')
  return client


# product fixture

@pytest.fixture
def category1(db):
    return Category.objects.create(name='Watch')

@pytest.fixture
def category2(db):
    return Category.objects.create(name='Mobile')


@pytest.fixture
def product(db, category2):
    image = SimpleUploadedFile(
      name='test.jpg',
      content=b'',   # khali file — sirf naam chahiye
      content_type='image/jpeg'
    )
    return Product.objects.create(
        name='Test Product',
        price=100.00,
        category=category2,
        description='latest',
        stock= 5,
        image=image,
    )

@pytest.fixture
def cart_with_item(user, product):
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product_id=product.id, quantity=2)
    return cart