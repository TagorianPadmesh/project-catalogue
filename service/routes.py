from flask import jsonify, request, abort
from service.models import Product, Category

def check_content_type(expected):
    if request.content_type != expected:
        abort(415, description=f"Content-Type must be {expected}")

def register_routes(app):
    @app.route("/products", methods=["POST"])
    def create_product():
        check_content_type("application/json")
        data = request.get_json()
        if not data:
            abort(400, description="Missing JSON body")
        try:
            product = Product(
                name=data["name"],
                description=data.get("description", ""),
                price=data["price"],
                available=data.get("available", True),
                category=Category[data.get("category", "UNKNOWN").upper()],
            )
            product.create()
        except (KeyError, ValueError, TypeError) as exc:
            abort(400, description=str(exc))
        return jsonify(product.serialize()), 201

    @app.route("/products/<int:product_id>", methods=["GET"])
    def read_product(product_id):
        product = Product.find(product_id)
        if product is None:
            return jsonify(message="Product not found"), 404
        return jsonify(product.serialize()), 200

    @app.route("/products/<int:product_id>", methods=["PUT"])
    def update_products(product_id):
        check_content_type("application/json")
        product = Product.find(product_id)
        if not product:
            abort(404, description=f"Product with id '{product_id}' was not found.")
        data = request.get_json()
        try:
            product.deserialize(data)
        except (KeyError, ValueError, TypeError) as exc:
            abort(400, description=str(exc))
        product.id = product_id
        product.update()
        return jsonify(product.serialize()), 200

    @app.route("/products/<int:product_id>", methods=["DELETE"])
    def delete_products(product_id):
        product = Product.find(product_id)
        if product:
            product.delete()
        return "", 204

    @app.route("/products", methods=["GET"])
    def list_products():
        name = request.args.get("name")
        category = request.args.get("category")
        available = request.args.get("available")
        if name:
            products = Product.find_by_name(name)
        elif category:
            try:
                category_value = getattr(Category, category.upper())
            except AttributeError:
                return jsonify([]), 200
            products = Product.find_by_category(category_value)
        elif available is not None:
            available_value = available.lower() in ["true", "yes", "1"]
            products = Product.find_by_availability(available_value)
        else:
            products = Product.all()
        return jsonify([product.serialize() for product in products]), 200
