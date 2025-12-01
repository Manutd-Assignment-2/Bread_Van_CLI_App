from App.database import db
from datetime import datetime
from typing import Dict

class Notification(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True)
    residentId = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    resident = db.relationship("Resident", backref="notifications")

    def __init__(self, resident_id: int, message: str):
        self.resident_id = resident_id
        self.message = message

    def get_json(self) -> Dict:
        return {"id": self.id, "resident_id": self.resident_id, "message": self.message, "date": self.date.isoformat()}
