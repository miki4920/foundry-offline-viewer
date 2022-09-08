import json
import os
from decimal import Decimal

from database import truncate_table


class CreateDatabase:
    def __init__(self, client):
        self.coin_dictionary = {"pp": 10, "gp": 1, "sp": 0.1, "cp": 0.01, }
        self.ids = ["AOh3phVs5PQ2Ae9A", "J5njm4YwaRu9sj3T", "v9KEi6wvQBIMIAAA", "aLgv3EleWVLOWT68", "MAi78zS5iDn4d5wp"]
        self.foundry_path = os.getenv("FOUNDRY_PATH")
        self.properties = self.get_properties()
        self.client = client
        truncate_table("characters")
        truncate_table("items")

    @staticmethod
    def get_properties():
        with open(os.getenv("PROPERTIES_PATH"), "r") as file:
            return json.load(file)

    def get_foundry_file(self):
        with open(self.foundry_path, "r", encoding="utf-8") as file:
            text = file.readlines()
        file = [json.loads(line) for line in text][::-1]
        return file

    def remove_duplicate_ids(self, json_file):
        unique_characters = []
        for line in json_file:
            if line["_id"] in self.ids:
                unique_characters.append(line)
                self.ids.remove(line["_id"])
        return unique_characters

    def check_if_item_has_runes(self, data, item_type):
        if data.get("specific") is not None and data["specific"]["value"]:
            return False
        for entry in data:
            if self.properties.get(item_type) and self.properties[item_type].get(entry) and data[entry]["value"]:
                return True
        return False

    def item_value_converter(self, data):
        item_type = data["type"]
        item_type = item_type if item_type == "armor" else "other"
        data = data["system"]
        level = data["level"]["value"]
        gold_value = 0
        for coin_type, coin_quantity in data["price"]["value"].items():
            gold_value += self.coin_dictionary[coin_type] * coin_quantity
        if self.check_if_item_has_runes(data, item_type):
            gold_value = 0
            for entry in data:
                if self.properties.get(item_type) and self.properties[item_type].get(entry) and data[entry]["value"]:
                    gold_value += self.properties[item_type][entry][str(data[entry]["value"])]["price"]
                    level = max(self.properties[item_type][entry][str(data[entry]["value"])]["level"], level)
        if data["price"].get("per"):
            gold_value /= data["price"]["per"]
        return json.loads(json.dumps(round(gold_value, 2)), parse_float=Decimal), level

    def insert_into_database(self):
        characters = self.remove_duplicate_ids(self.get_foundry_file())
        count = 0
        for character in characters:
            items = character["items"]
            item_ids = []
            for item in items:
                if item["system"].get("price") and item["system"].get("quantity") and "infused" not in item["system"]["traits"]["value"]:
                    item_value, level = self.item_value_converter(item)
                    consumable = "consumable" in item["system"]["traits"]["value"]
                    self.client.put_item(TableName='items', Item={
                        'id': {"N": str(count)},
                        'name': {"S": item["name"]},
                        'level': {"S": str(level)},
                        'value': {"S": str(item_value)},
                        'quantity': {"S": str(item["system"]["quantity"])},
                        'total': {"S": str(item["system"]["quantity"] * item_value)},
                        'consumable': {"N": str(int(consumable))}
                    })
                    item_ids.append(str(count))
                    count += 1
            self.client.put_item(TableName='characters', Item={
                'name': {"S": character["name"]},
                'items': {"NS": item_ids}
            })



