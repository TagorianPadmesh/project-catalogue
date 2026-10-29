from behave import given
import requests

@given("the following products")
def step_load_products(context):
    for row in context.table:
        product_data = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "category": row["category"],
            "available": row["available"].lower() == "true",
        }
        response = requests.post(
            f"{context.base_url}/products",
            json=product_data,
        )
        assert response.status_code in (200, 201)
