from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from typing import Dict

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    logged_in = db.Column(db.Boolean, nullable=False, default=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "user"
    }

    def __init__(self, username: str, password: str):
        self.username = username
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def login(self, password: str) -> bool:
        if self.check_password(password):
            self.logged_in = True
            db.session.commit()
            return True
        return False

    def logout(self) -> None:
        self.logged_in = False
        db.session.commit()

    def get_json(self) -> Dict:
        return {"id": self.id, "username": self.username, "type": self.type}
