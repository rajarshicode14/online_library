from website import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact_no = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.Integer, db.ForeignKey(
        "user_type.id"), nullable=False)

    def __init__(self, full_name, email, contact_no, country, password, user_type):
        self.full_name = full_name
        self.email = email
        self.contact_no = contact_no
        self.country = country
        self.password = password
        self.user_type = user_type

    def is_user(self):
        return True

    def is_library(self):
        return False
