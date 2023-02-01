from website import db
from flask_login import UserMixin


class UserType(db.Model, UserMixin):
    __tablename__ = 'user_type'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", backref="user")
    library = db.relationship("Library", backref="library")

    def __init__(self, type):
        self.type = type
