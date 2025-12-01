from App.database import db
from .user import User

class Admin(db.Model, User):
    __tablename__ = "admin"

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "Admin"}

    def __init__(self, username: str, password: str):
        User.__init__(self, username, password)

    def get_json(self):
        return User.get_json(self)
