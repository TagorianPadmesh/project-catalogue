from service.models import Product
from tests.factories import ProductFactory

def persist(product):
    product.id = None
    product.create()
    return product

def test_read_a_product(app):
    product = persist(ProductFactory())
    found = Product.find(product.id)
    assert found is not None
    assert found.id == product.id
    assert found.name == product.name
    assert found.description == product.description
    assert float(found.price) == float(product.price)

def test_update_a_product(app):
    product = persist(ProductFactory())
    original_id = product.id
    product.description = "testing"
    product.update()
    assert product.id == original_id
    assert product.description == "testing"
    products = Product.all()
    assert len(products) == 1
    assert products[0].id == original_id
    assert products[0].description == "testing"

def test_delete_a_product(app):
    product = persist(ProductFactory())
    assert len(Product.all()) == 1
    product.delete()
    assert len(Product.all()) == 0

def test_list_all_products(app):
    assert Product.all() == []
    for _ in range(5):
        persist(ProductFactory())
    assert len(Product.all()) == 5

def test_find_by_name(app):
    products = [persist(ProductFactory()) for _ in range(5)]
    name = products[0].name
    expected = len([p for p in products if name.lower() in p.name.lower()])
    found = Product.find_by_name(name)
    assert len(found) == expected
    assert all(name.lower() in p.name.lower() for p in found)

def test_find_by_category(app):
    products = [persist(ProductFactory()) for _ in range(10)]
    category = products[0].category
    expected = len([p for p in products if p.category == category])
    found = Product.find_by_category(category)
    assert len(found) == expected
    assert all(p.category == category for p in found)

def test_find_by_availability(app):
    products = [persist(ProductFactory()) for _ in range(10)]
    available = products[0].available
    expected = len([p for p in products if p.available == available])
    found = Product.find_by_availability(available)
    assert len(found) == expected
    assert all(p.available == available for p in found)
