from App.database import db
from typing import Dict

class Stop(db.Model):
    __tablename__ = "stop"

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)

    route = db.relationship('Route', back_populates='stops')
    resident = db.relationship('Resident', back_populates='stops')

    def __init__(self, resident_id: int, route_id: int = None):
        self.resident_id = resident_id
        self.route_id = route_id

    def get_json(self) -> Dict:
        return {"id": self.id, "route_id": self.route_id, "resident_id": self.resident_id}
