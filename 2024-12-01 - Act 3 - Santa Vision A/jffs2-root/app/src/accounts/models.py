from datetime import datetime

from flask_login import UserMixin

from src import db


class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.created_on = datetime.now()
        self.is_admin = is_admin

    def __repr__(self):
        return f"<username {self.username}>"
