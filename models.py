# models.py
from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    roles = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Post {self.id}>'

class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.roles = users[username]['roles']

def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None