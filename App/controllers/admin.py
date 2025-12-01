from App.database import db
from App.models.admin import Admin
from App.models.driver import Driver
from App.models.area import Area
from App.models.street import Street
from sqlalchemy.exc import IntegrityError

class AdminController:
    @staticmethod
    def create_driver(username: str, password: str, status: str = "Offline", area_id: int = None, street_id: int = None):
        d = Driver(username=username, password=password, status=status, area_id=area_id, street_id=street_id)
        try:
            db.session.add(d)
            db.session.commit()
            return d
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def delete_driver(driver_id: int):
        driver = Driver.query.get(driver_id)
        if not driver:
            return False
        try:
            db.session.delete(driver)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def add_area(name: str):
        a = Area(name=name)
        try:
            db.session.add(a)
            db.session.commit()
            return a
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def delete_area(area_id: int):
        a = Area.query.get(area_id)
        if not a: return False
        try:
            db.session.delete(a)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def add_street(area_id: int, name: str):
        area = Area.query.get(area_id)
        if not area:
            return None
        s = Street(name=name, area_id=area_id)
        try:
            db.session.add(s)
            db.session.commit()
            return s
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def delete_street(street_id: int):
        s = Street.query.get(street_id)
        if not s: return False
        try:
            db.session.delete(s)
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    @staticmethod
    def view_all_areas():
        return Area.query.all()

    @staticmethod
    def view_all_streets():
        return Street.query.all()
