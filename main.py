from flask import render_template

from update_file import app, db, Character


@app.route("/")
def main_app():
    characters = Character.query.order_by(Character.name).all()
    wealth = []
    wealth_without_consumable = []
    for character in characters:
        value = 0
        value_consumables = 0
        for item in character.items:
            item_value = item.value * item.quantity
            if item.consumable:
                value_consumables += item_value
            else:
                value += item_value
        wealth.append((round(value + value_consumables, 2), character.name))
        wealth_without_consumable.append((round(value, 2), character.name))
    character_names = [character.name for character in characters]
    wealth = list(zip(*sorted(wealth, reverse=True)))
    wealth_without_consumable = list(zip(*sorted(wealth_without_consumable, reverse=True)))
    return render_template("index.html", characters=character_names, wealth=wealth, wealth_without_consumable=wealth_without_consumable)