from App.database import db
from App.models.resident import Resident
from App.models.stop import Stop
from sqlalchemy.exc import IntegrityError

class ResidentController:
    @staticmethod
    def create_resident(username: str, password: str, area_id: int, street_id: int, house_number: int):
        r = Resident(username=username, password=password, area_id=area_id, street_id=street_id, house_number=house_number)
        try:
            db.session.add(r)
            db.session.commit()
            return r
        except IntegrityError:
            db.session.rollback()
            raise

    @staticmethod
    def request_stop(resident_id: int, route_id: int = None):
        r = Resident.query.get(resident_id)
        if not r:
            return None
        try:
            s = Stop(resident_id=resident_id, route_id=route_id)
            db.session.add(s)
            db.session.commit()
            return s
        except Exception:
            db.session.rollback()
            return None

    @staticmethod
    def view_inbox(resident_id: int):
        r = Resident.query.get(resident_id)
        if not r:
            return []
        return r.inbox
