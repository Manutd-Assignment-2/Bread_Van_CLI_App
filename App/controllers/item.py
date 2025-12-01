from App.database import db
from App.models.item import Item
from sqlalchemy.exc import IntegrityError

class ItemController:
    @staticmethod
    def create_item(name: str, price: float, description: str = "", tags: list = None):
        item = Item(name=name, price=price, description=description, tags=tags or [])
        try:
            db.session.add(item)
            db.session.commit()
            return item
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def update_price(item_id: int, new_price: float):
        item = Item.query.get(item_id)
        if not item:
            return None
        try:
            item.update_price(new_price)
            db.session.commit()
            return item
        except Exception:
            db.session.rollback()
            raise
