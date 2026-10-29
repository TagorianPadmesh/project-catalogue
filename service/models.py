from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(Enum):
    UNKNOWN = "Unknown"
    CLOTHS = "Cloths"
    FOOD = "Food"
    HOUSEWARES = "Housewares"
    TOOLS = "Tools"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False, default="")
    price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    available = db.Column(db.Boolean, nullable=False, default=True)
    category = db.Column(db.Enum(Category), nullable=False, default=Category.UNKNOWN)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "available": self.available,
            "category": self.category.name,
        }

    def deserialize(self, data):
        for key in ("name", "description", "price", "available"):
            if key in data:
                setattr(self, key, data[key])
        if "category" in data:
            value = data["category"]
            self.category = value if isinstance(value, Category) else Category[value.upper()]
        return self

    @classmethod
    def find(cls, product_id):
        return cls.query.get(product_id)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(f"%{name}%")).all()

    @classmethod
    def find_by_category(cls, category):
        if isinstance(category, str):
            category = Category[category.upper()]
        return cls.query.filter_by(category=category).all()

    @classmethod
    def find_by_availability(cls, available):
        return cls.query.filter_by(available=available).all()
