from flask import render_template, Flask, redirect
from common.model import fetch_characters

character_colours = ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)',
                     'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)',
                     'rgba(153, 102, 255, 0.2)']
app = Flask("app")


def unzip_list(zipped_list):
    return list(zip(*sorted(zipped_list, reverse=True)))


def get_wealth(characters):
    wealth = []
    for i, character in enumerate(characters):
        wealth.append(
            (round(sum([item["value"] * item["quantity"] for item in character["items"]]), 2), character["name"],
             character_colours[i]))
    return unzip_list(wealth)


def get_wealth_without_consumables(characters):
    wealth_without_consumables = []
    for i, character in enumerate(characters):
        wealth_without_consumables.append((round(
            sum([item["value"] * item["quantity"] for item in character["items"] if not item["consumable"]]), 2),
                                           character["name"], character_colours[i]))
    return unzip_list(wealth_without_consumables)


def get_highest_item_level(characters):
    highest_item_level = []
    for i, character in enumerate(characters):
        highest_item_level.append(
            (max([item["level"] for item in character["items"]]), character["name"], character_colours[i]))
    return unzip_list(highest_item_level)


@app.route("/")
def home():
    return redirect("/Treasury")


@app.route("/<current_character>")
def main(current_character):
    characters = fetch_characters()
    wealth = get_wealth(characters)
    wealth_without_consumable = get_wealth_without_consumables(characters)
    return render_template("index.html", current_character=current_character, characters=characters, wealth=wealth,
                           wealth_without_consumable=wealth_without_consumable)
