from website import db
from flask_login import UserMixin


class Books(db.Model, UserMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100))
    edition = db.Column(db.String(100))
    library_name = db.Column(db.String(250), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    issued_count = db.Column(db.Integer, nullable=False)
    library_id = db.Column(db.Integer, db.ForeignKey("library.id"))

    def __init__(self, title, author, publisher, edition, library_name, genre, issued_count, library_id):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.edition = edition
        self.library_name = library_name
        self.genre = genre
        self.issued_count = issued_count
        self.library_id = library_id
