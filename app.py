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
    data = sorted(data, key=lambda character_json: (character_json["priority"], character_json["name"]))
    response = flask.jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

