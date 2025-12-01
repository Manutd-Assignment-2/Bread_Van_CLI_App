from App.database import db
from typing import Dict

class Route(db.Model):
    __tablename__ = "route"

    id = db.Column(db.Integer, primary_key=True)
    scheduled_driver = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    scheduled_date = db.Column(db.Date, nullable=True)
    scheduled_time = db.Column(db.Time, nullable=True)
    scheduled_area = db.Column(db.String(100), nullable=True)
    scheduled_street = db.Column(db.String(100), nullable=True)
    eta = db.Column(db.String(50))   
    menu = db.Column(db.JSON) 
    stops = db.relationship('Stop', back_populates='route', cascade='all, delete-orphan', lazy='joined')
    driver = db.relationship('Driver', back_populates='routes')

    def __init__(self, scheduled_driver: int, scheduled_date=None, scheduled_time=None, scheduled_area: str = None, scheduled_street: str = None):
        self.scheduled_driver = scheduled_driver
        self.scheduled_date = scheduled_date
        self.scheduled_time = scheduled_time
        self.scheduled_area = scheduled_area
        self.scheduled_street = scheduled_street

    def get_json(self) -> Dict:
        return {
            "id": self.id,
            "scheduled_driver": self.scheduled_driver,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "scheduled_area": self.scheduled_area,
            "scheduled_street": self.scheduled_street,
            "stops": [s.get_json() for s in self.stops]
        }
