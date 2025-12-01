from App.database import db
from sqlalchemy import JSON
from typing import Dict, Optional

class Item(db.Model):
    __tablename__ = "item"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    tags = db.Column(JSON, nullable=True, default=[])

    def __init__(self, name: str, price: float, description: str = "", tags: Optional[list] = None):
        self.name = name
        self.price = price
        self.description = description
        self.tags = tags or []

    def get_json(self) -> Dict:
        return {"id": self.id, "name": self.name, "price": self.price, "description": self.description, "tags": self.tags}

    def update_price(self, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price
