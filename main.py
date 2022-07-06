from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template("index.html", characters=["Lizzie", "Jean", "Reiner", "Quamnious", "Treasury"], current_character="All Characters")