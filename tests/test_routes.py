from service.models import Product
from tests.factories import ProductFactory

BASE_URL = "/products"

def create_products(client, count):
    products = []
    for _ in range(count):
        p = ProductFactory()
        payload = {
            "name": p.name, "description": p.description,
            "price": float(p.price), "available": p.available,
            "category": p.category.name,
        }
        response = client.post(BASE_URL, json=payload)
        assert response.status_code == 201
        products.append(response.get_json())
    return products

def test_get_product(client):
    product = create_products(client, 1)[0]
    response = client.get(f"{BASE_URL}/{product['id']}")
    assert response.status_code == 200
    assert response.get_json()["name"] == product["name"]

def test_update_product(client):
    product = create_products(client, 1)[0]
    product["description"] = "unknown"
    response = client.put(f"{BASE_URL}/{product['id']}", json=product)
    assert response.status_code == 200
    assert response.get_json()["description"] == "unknown"

def test_delete_product(client):
    products = create_products(client, 5)
    product_id = products[0]["id"]
    response = client.delete(f"{BASE_URL}/{product_id}")
    assert response.status_code == 204
    assert response.data == b""
    assert client.get(f"{BASE_URL}/{product_id}").status_code == 404
    assert len(client.get(BASE_URL).get_json()) == 4

def test_get_product_list(client):
    create_products(client, 5)
    response = client.get(BASE_URL)
    assert response.status_code == 200
    assert len(response.get_json()) == 5

def test_query_by_name(client):
    products = create_products(client, 5)
    test_name = products[0]["name"]
    expected = sum(1 for p in products if test_name.lower() in p["name"].lower())
    response = client.get(BASE_URL, query_string={"name": test_name})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == expected
    assert all(test_name.lower() in p["name"].lower() for p in data)

def test_query_by_category(client):
    products = create_products(client, 10)
    category = products[0]["category"]
    expected = sum(1 for p in products if p["category"] == category)
    response = client.get(BASE_URL, query_string={"category": category})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == expected
    assert all(p["category"] == category for p in data)

def test_query_by_availability(client):
    products = create_products(client, 10)
    expected = sum(1 for p in products if p["available"] is True)
    response = client.get(BASE_URL, query_string={"available": "true"})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == expected
    assert all(p["available"] is True for p in data)
