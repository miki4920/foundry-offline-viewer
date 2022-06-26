import json

ids = ["AOh3phVs5PQ2Ae9A", "J5njm4YwaRu9sj3T", "MAi78zS5iDn4d5wp", "v9KEi6wvQBIMIAAA", "aLgv3EleWVLOWT68"]


with open(r"C:\Users\Mikolaj Grobelny\AppData\Local\FoundryVTT\Data\worlds\darklands\data\actors.db", "r") as file:
    file = file.read().split("\n")[:-1]
    file = [json.loads(line) for line in file]
    characters = []
    for line in file:
        if line["_id"] in ids:
            characters.append(line)
            ids.remove(line["_id"])
    for character in characters:
        pass
    character_one = characters[0]["items"]
    counter = 0
    for x in character_one:
        if x["data"].get("price"):
            counter+= 1
    with open("test.json", "w") as f:
        json.dump(characters, f, indent=4)
