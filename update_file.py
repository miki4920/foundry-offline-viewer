import json

price = {"pp": 10, "gp": 1, "sp": 0.1, "cp": 0.01, }
ids = ["AOh3phVs5PQ2Ae9A", "J5njm4YwaRu9sj3T", "MAi78zS5iDn4d5wp", "v9KEi6wvQBIMIAAA", "aLgv3EleWVLOWT68"]
foundry_file = r"C:\Users\Mikolaj Grobelny\AppData\Local\FoundryVTT\Data\worlds\darklands\data\actors.db"
character_file = "character_equipment.json"


def remove_duplicate_ids(json_file):
    unique_characters = []
    for line in json_file:
        if line["_id"] in ids:
            unique_characters.append(line)
            ids.remove(line["_id"])
    return unique_characters


def get_character_dictionary(character_json_file):
    dictionary = {}
    for character in character_json_file:
        items = []
        for item in character["items"]:
            if item["data"].get("price"):
                items.append({"name": item["name"], "description": item["data"]["description"],
                              "price": item["data"]["price"]["value"], "quantity": item["data"]["quantity"]})
        dictionary[character["name"]] = items
    return dictionary


def get_foundry_file():
    with open(foundry_file, "r") as file:
        file = file.read().split("\n")[:-1]
        file = [json.loads(line) for line in file]
    return file


characters = remove_duplicate_ids(get_foundry_file())
characters_dictionary = get_character_dictionary(characters)
with open(character_file, "w") as f:
    json.dump(characters_dictionary, f, indent=4)
