from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    characters_wealth_tuples = sorted([(149.73, "Jean"), (130.10, "Lizzie"), (100.50, "Quamnious"), (119.32, "Reiner"), (50.4, "Treasury")], reverse=True)
    characters = [pair[1] for pair in characters_wealth_tuples]
    wealth = [pair[0] for pair in characters_wealth_tuples]
    return render_template("index.html", current_character="All Characters", characters=characters, wealth=wealth)