from src import db
import re


class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    articles = db.relationship('posts', backref='user', lazy=True)


class posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
