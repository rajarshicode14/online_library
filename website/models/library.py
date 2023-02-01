from website import db
from flask_login import UserMixin


class Library(db.Model, UserMixin):
    __tablename__ = 'library'

    id = db.Column(db.Integer, primary_key=True)
    library_name = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    registration_no = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    books = db.relationship("Books", backref="library")
    user_type = db.Column(db.Integer, db.ForeignKey(
        "user_type.id"), nullable=False)

    def __init__(self, library_name, address, postal_code, contact_no, email, registration_no, password, user_type):
        self.library_name = library_name
        self.address = address
        self.postal_code = postal_code
        self.contact_no = contact_no
        self.email = email
        self.registration_no = registration_no
        self.password = password
        self.user_type = user_type

    def is_library(self):
        return True

    def is_user(self):
        return False
