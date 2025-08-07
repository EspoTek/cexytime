from mongoengine import Document, StringField
from flask_login import UserMixin

class User(Document, UserMixin):
    email = StringField(required=True, unique=True)  # User's email address
    password_hash = StringField(required=True)  # Hashed password
