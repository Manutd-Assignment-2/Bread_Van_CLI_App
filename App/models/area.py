from App.database import db

class Area(db.Model):
    __tablename__ = "area"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    streets = db.relationship("Street", back_populates="area", cascade="all, delete-orphan")
    residents = db.relationship("Resident", back_populates="area", lazy="dynamic")
    drivers = db.relationship("Driver", back_populates="area", lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def get_json(self):
        return {"id": self.id, "name": self.name}
