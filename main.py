import json

ids = ["AOh3phVs5PQ2Ae9A", "J5njm4YwaRu9sj3T", "MAi78zS5iDn4d5wp", "v9KEi6wvQBIMIAAA", "aLgv3EleWVLOWT68"]
price = {"pp": 10, "gp": 1, "sp": 0.1, "cp": 0.01, }

with open(r"C:\Users\Mikolaj Grobelny\AppData\Local\FoundryVTT\Data\worlds\darklands\data\actors.db", "r") as file:
    file = file.read().split("\n")[:-1]
    file = [json.loads(line) for line in file]
    characters = []
    characters_dictionary = {}
    for line in file:
        if line["_id"] in ids:
            characters.append(line)
            ids.remove(line["_id"])
    for character in characters:
        items = []
        for item in character["items"]:
            if item["data"].get("price"):
                items.append({"name": item["name"], "description": item["data"]["description"], "price": item["data"]["price"]["value"], "quantity": item["data"]["quantity"]})
        characters_dictionary[character["name"]] = items
    with open("test.json", "w") as f:
        json.dump(characters_dictionary, f, indent=4)
