import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config["DATABASE_NAME"] = os.getenv("DATABASE_NAME")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://' + app.config["DATABASE_NAME"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Character %r>' % self.name


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