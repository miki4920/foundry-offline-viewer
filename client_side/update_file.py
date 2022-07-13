import json
import os
from decimal import Decimal

from common.model import create_table


class CreateDatabase:
    def __init__(self, client):
        self.coin_dictionary = {"pp": 10, "gp": 1, "sp": 0.1, "cp": 0.01, }
        self.ids = ["AOh3phVs5PQ2Ae9A", "J5njm4YwaRu9sj3T", "MAi78zS5iDn4d5wp", "v9KEi6wvQBIMIAAA", "aLgv3EleWVLOWT68"]
        self.foundry_path = os.getenv("FOUNDRY_PATH")
        self.properties_path = os.getenv("PROPERTIES_PATH")
        self.properties = self.get_properties()
        self.client = client
        self.truncate_table("characters")
        self.truncate_table("items")
        create_table()

    def truncate_table(self, table):
        self.client.delete_table(TableName=table)
        waiter = self.client.get_waiter('table_not_exists')
        waiter.wait(TableName=table)

    def get_properties(self):
        with open(self.properties_path, "r") as file:
            return json.load(file)

    def get_foundry_file(self):
        with open(self.foundry_path, "r") as file:
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

    def item_value_converter(self, data):
        gold_value = 0
        level = data["level"]["value"]
        for entry in data:
            if self.properties.get(entry) and data[entry]["value"]:
                gold_value += self.properties[entry][str(data[entry]["value"])]["price"]
                level = max(self.properties[entry][str(data[entry]["value"])]["level"], level)
        for coin_type, coin_quantity in data["price"]["value"].items():
            gold_value += self.coin_dictionary[coin_type] * coin_quantity
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
                if item["data"].get("price") and item["data"].get("quantity") and "infused" not in item["data"]["traits"]["value"]:
                    item_value, level = self.item_value_converter(item["data"])
                    consumable = "consumable" in item["data"]["traits"]["value"]
                    self.client.put_item(TableName='items', Item={
                        'id': {"N": str(count)},
                        'name': {"S": item["name"]},
                        'description': {"S": item["data"]["description"]["value"]},
                        'level': {"N": str(level)},
                        'value': {"N": str(item_value)},
                        'quantity': {"N": str(item["data"]["quantity"])},
                        'consumable': {"N": str(int(consumable))}
                    })
                    item_ids.append(str(count))
                    count += 1
            self.client.put_item(TableName='characters', Item={
                'name': {"S": character["name"]},
                'items': {"NS": item_ids}
            })



