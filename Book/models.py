from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)
class Book(db.Model, UserMixin):
    __tablename__ = 'books'
    isbn = db.Column('ISBN', db.String(13), primary_key=True, nullable=False, unique=True)  # Column name is 'ISBN'
    title = db.Column('Book-Title', db.String(25), nullable=True)  # Column name is 'Book-Title'
    author = db.Column('Book-Author', db.String(255), nullable=True)  # Column name is 'Book-Author'
    year_of_publication = db.Column('Year-Of-Publication', db.Integer,nullable=True)  # Column name is 'Year-Of-Publication'
    publisher = db.Column('Publisher', db.String(255), nullable=True)  # Column name is 'Publisher'
    image_url_s = db.Column('Image-URL-S', db.String(255), nullable=True)  # Column name is 'Image-URL-S'
    image_url_m = db.Column('Image-URL-M', db.String(255), nullable=True)  # Column name is 'Image-URL-M'
    image_url_l = db.Column('Image-URL-L', db.String(255), nullable=True)  # Column name is 'Image-URL-L'


    def __repr__(self):
        return f'<Book {self.isbn} {self.title}>'

    def serialize(self):
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'year_of_publication': self.year_of_publication,
            'publisher': self.publisher,
            'image_url_s': self.image_url_s,
            'image_url_m': self.image_url_m,
            'image_url_l': self.image_url_l,
        }
