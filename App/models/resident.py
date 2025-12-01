from App.database import db
from datetime import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import JSON
from .observer import Observer
from typing import List, Dict, Optional

MAX_INBOX_SIZE = 20

class Resident(db.Model, Observer):
    __tablename__ = "resident"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    house_number = db.Column(db.Integer, nullable=False)
    inbox = db.Column(MutableList.as_mutable(JSON), default=list)

    area = db.relationship("Area", back_populates="residents")
    street = db.relationship("Street", back_populates="residents")
    stops = db.relationship('Stop', back_populates='resident', cascade='all, delete-orphan', lazy='dynamic')
    notifications = db.relationship('Notification', back_populates='resident', cascade='all, delete-orphan', lazy='dynamic')

    __mapper_args__ = {"polymorphic_identity": "Resident"}

    def __init__(self, username: str, password: str, area_id: int, street_id: int, house_number: int):
        from .user import User
        User.__init__(self, username, password)
        self.area_id = area_id
        self.street_id = street_id
        self.house_number = house_number
        self.inbox = []

    def update(self, subject, message: str):
        self.receive_notif(message)

    def receive_notif(self, message: str) -> None:
        if self.inbox is None:
            self.inbox = []
        if len(self.inbox) >= MAX_INBOX_SIZE:
            self.inbox.pop(0)
        timestamp = datetime.utcnow().strftime("%Y:%m:%d:%H:%M:%S")
        notif = f"[{timestamp}]: {message}"
        self.inbox.append(notif)
        # persist a Notification object as well for history
        try:
            from .notification import Notification
            n = Notification(resident_id=self.id, message=message)
            db.session.add(self)
            db.session.add(n)
            db.session.commit()
        except Exception:
            db.session.rollback()

    def get_json(self) -> Dict:
        from .user import User
        user_json = User.get_json(self)
        user_json.update({"area_id": self.area_id, "street_id": self.street_id, "house_number": self.house_number, "inbox": self.inbox})
        return user_json

    def request_stop(self, route_id: int = None):
        from .stop import Stop
        try:
            new_stop = Stop(resident_id=self.id, route_id=route_id)
            db.session.add(new_stop)
            db.session.commit()
            return new_stop
        except Exception:
            db.session.rollback()
            return None
