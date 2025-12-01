from App.database import db

class Street(db.Model):
    __tablename__ = "street"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)

    area = db.relationship("Area", back_populates="streets")
    residents = db.relationship("Resident", back_populates="street", cascade="all, delete-orphan", lazy="dynamic")
    drivers = db.relationship("Driver", back_populates="street", lazy="dynamic")

    def __init__(self, name: str, area_id: int):
        self.name = name
        self.area_id = area_id

    def get_json(self):
        return {"id": self.id, "name": self.name, "area_id": self.area_id}
