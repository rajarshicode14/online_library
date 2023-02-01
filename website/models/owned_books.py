from website import db
from flask_login import UserMixin


class OwnedBooks(db.Model, UserMixin):
    __tablename__ = 'owned_books'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    is_read = db.Column(db.Boolean)

    def __init__(self, user_id, book_id, is_read):
        self.user_id = user_id
        self.book_id = book_id
        self.is_read = False
