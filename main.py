from flask import render_template

from update_file import app, db, Character


@app.route("/")
def main_app():
    characters = Character.query.order_by(Character.name).all()
    character_names = [character.name for character in characters]
    wealth = [round(sum([item.value * item.quantity for item in character.items]), 2) for character in characters]
    return render_template("index.html", current_character="All Characters", characters=character_names, wealth=wealth)