from flask import render_template, Flask, redirect, send_from_directory
from flask_restful import Api

from database import fetch_characters
from database_api import WealthApiHandler

app = Flask("app", static_folder='frontend/build')
api = Api(app)


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(WealthApiHandler, '/wealth')
