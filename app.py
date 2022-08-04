import flask
from flask import Flask

from database import fetch_data


app = Flask("app", static_folder='frontend/build', static_url_path="/")


@app.route("/")
def serve():
    return app.send_static_file('index.html')


@app.get("/wealth")
def get():
    data = fetch_data()
    treasury = {}
    for i, character_json in enumerate(data):
        if character_json["name"] == "Treasury":
            treasury = character_json
            del data[i]
    data = sorted(data, key=lambda character_json: character_json["name"])
    data.insert(0, treasury)
    response = flask.jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

