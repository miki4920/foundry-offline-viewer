import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask("app")
app.config['SQLALCHEMY_DATABASE_URI'] = f"amazondynamodb:///?Access Key={os.getenv('ACCESS_KEY')}&Secret Key={os.getenv('SECRET_KEY')}&Domain=amazonaws.com&Region={os.getenv('REGION')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("character.id"), nullable=False)
    owner = db.relationship("Character", backref=db.backref('items', lazy="dynamic"))
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    level = db.Column(db.SmallInteger, nullable=False)
    value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.SmallInteger, nullable=False)
    consumable = db.Column(db.Boolean, nullable=False)