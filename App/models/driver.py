from App.database import db
from typing import List, Optional
from .subject import Subject
from .user import User

class Driver(db.Model, User, Subject):
    __tablename__ = "driver"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    status = db.Column(db.String(20), nullable=False, default="Offline")
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=True)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=True)

    area = db.relationship("Area", back_populates="drivers")
    street = db.relationship("Street", back_populates="drivers")
    drives = db.relationship('Drive', back_populates='driver', cascade='all, delete-orphan', lazy='dynamic')
    routes = db.relationship('Route', back_populates='driver', lazy='dynamic')

    __mapper_args__ = {"polymorphic_identity": "Driver"}

    # in-memory observer list (not persisted) - optional extra observers
    _observers: List = []

    def __init__(self, username: str, password: str, status: str = "Offline", area_id: Optional[int] = None, street_id: Optional[int] = None):
        User.__init__(self, username, password)
        self.status = status
        self.area_id = area_id
        self.street_id = street_id
        self._observers = []

    def get_json(self):
        base = User.get_json(self)
        base.update({"status": self.status, "area_id": self.area_id, "street_id": self.street_id})
        return base

    # Subject interface (optional: also notify street residents)
    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, message: str):
        # notify in-memory observers
        for o in list(self._observers):
            try:
                o.update(self, message)
            except Exception:
                pass

        # also notify residents on the same street (if linked) — persistent
        if self.street is not None:
            for resident in self.street.residents:
                try:
                    resident.update(self, message)
                except Exception:
                    pass
