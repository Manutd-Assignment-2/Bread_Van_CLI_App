from App.database import db
from datetime import date, time
from typing import Dict

class Drive(db.Model):
    __tablename__ = "drive"

    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=True)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=True)
    date = db.Column(db.Date, nullable=True)
    time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="Upcoming")

    driver = db.relationship('Driver', back_populates='drives')

    def __init__(self, driver_id: int, area_id: int = None, street_id: int = None, date: date = None, time: time = None, status: str = "Upcoming"):
        self.driver_id = driver_id
        self.area_id = area_id
        self.street_id = street_id
        self.date = date
        self.time = time
        self.status = status

    def get_json(self) -> Dict:
        return {"id": self.id, "driver_id": self.driver_id, "area_id": self.area_id, "street_id": self.street_id, "date": self.date.isoformat() if self.date else None, "time": self.time.isoformat() if self.time else None, "status": self.status}
