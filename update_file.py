import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wealth.db'
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
    owner = db.relationship("Character", backref=db.backref('items', lazy=True))
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    level = db.Column(db.SmallInteger, nullable=False)
    value = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.SmallInteger, nullable=False)
    consumable = db.Column(db.Boolean, nullable=False)


class CreateDatabase:
    def __init__(self):
        self.coin_dictionary = {"pp": 10, "gp": 1, "sp": 0.1, "cp": 0.01, }
        self.ids = ["AOh3phVs5PQ2Ae9A", "J5njm4YwaRu9sj3T", "MAi78zS5iDn4d5wp", "v9KEi6wvQBIMIAAA", "aLgv3EleWVLOWT68"]
        self.foundry_path = r"C:\Users\Mikolaj Grobelny\AppData\Local\FoundryVTT\Data\worlds\darklands\data\actors.db"

    def get_foundry_file(self):
        with open(self.foundry_path, "r") as file:
            file = file.read().split("\n")[:-1]
            file = [json.loads(line) for line in file]
        return file

    def remove_duplicate_ids(self, json_file):
        unique_characters = []
        for line in json_file:
            if line["_id"] in self.ids:
                unique_characters.append(line)
                self.ids.remove(line["_id"])
        return unique_characters

    def item_value_converter(self, price):
        gold_value = 0
        for coin_type, coin_quantity in price["value"].items():
            gold_value += self.coin_dictionary[coin_type] * coin_quantity
        if price.get("per"):
            gold_value /= price["per"]
        return gold_value

    def insert_into_database(self, db):
        characters = self.remove_duplicate_ids(self.get_foundry_file())
        for character in characters:
            items = character["items"]
            character = Character(name=character["name"])
            db.session.add(character)
            for item in items:
                if item["data"].get("price") and "infused" not in item["data"]["traits"]["value"]:
                    item_value = round(self.item_value_converter(item["data"]["price"]), 2)
                    consumable = "consumable" in item["data"]["traits"]["value"]
                    item = Item(owner=character, name=item["name"], description=item["data"]["description"]["value"],
                                level=item["data"]["level"]["value"], value=item_value,
                                quantity=item["data"]["quantity"], consumable=consumable)
                    db.session.add(item)
            db.session.commit()


db.create_all()
db.drop_all()
db.create_all()

CreateDatabase().insert_into_database(db)

