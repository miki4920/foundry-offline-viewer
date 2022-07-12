from flask import request, render_template
from werkzeug.datastructures import FileStorage

from common.model import app, Character

character_colours = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)',
                     'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)',
                     'rgba(153, 102, 255, 0.2)']


def unzip_list(zipped_list):
    return list(zip(*sorted(zipped_list, reverse=True)))


def get_wealth(characters):
    wealth = []
    for i, character in enumerate(characters):
        wealth.append((round(sum([item.value * item.quantity for item in character.items]), 2), character.name,
                       character_colours[i]))
    return unzip_list(wealth)


def get_wealth_without_consumables(characters):
    wealth_without_consumables = []
    for i, character in enumerate(characters):
        wealth_without_consumables.append((round(
            sum([item.value * item.quantity for item in character.items.filter_by(consumable=False)]), 2),
                                           character.name, character_colours[i]))
    return unzip_list(wealth_without_consumables)


def get_highest_item_level(characters):
    highest_item_level = []
    for i, character in enumerate(characters):
        highest_item_level.append((max([item.level for item in character.items]), character.name, character_colours[i]))
    return unzip_list(highest_item_level)


@app.route("/")
def main_app():
    characters = Character.query.order_by(Character.name).all()
    wealth = get_wealth(characters)
    wealth_without_consumable = get_wealth_without_consumables(characters)
    character_names = [character.name for character in characters]
    return render_template("index.html", characters=character_names, wealth=wealth,
                           wealth_without_consumable=wealth_without_consumable)


@app.route("/upload", methods=['POST'])
def upload_file():
    FileStorage(request.stream).save(app.config["DATABASE_NAME"])
    return 'OK', 200
