import pytest
from products.models import Product, Category


# ---- Category ----
@pytest.mark.django_db
def test_category_str(category2):
    assert str(category2) == 'Mobile'

# ---- Product ----
@pytest.mark.django_db
def test_product_str(product):
    assert str(product) == 'Test Product'

@pytest.mark.django_db
def test_product_has_correct_price(product):
    assert product.price == 100.00

@pytest.mark.django_db
def test_product_belongs_to_category(product, category2):
    assert product.category == category2

@pytest.mark.django_db
def test_product_stock(product):
    assert product.stock == 5

@pytest.mark.django_db
def test_product_image_optional(category2):
    # image blank=True, null=True
    product = Product.objects.create(
        name='No Image Product',
        description='Test',
        price=50.00,
        category=category2,
        stock=5,
        image=None
    )
    assert product.image.name is None

@pytest.mark.django_db
def test_category_has_products(product, category2):
    # related_name='products'
    assert category2.products.filter(id=product.id).exists()

@pytest.mark.django_db
def test_product_filter_by_category(product, category2):

    products = Product.objects.filter(category__name__iexact='Mobile')
    assert product in products