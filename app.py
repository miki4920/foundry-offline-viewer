from flask import Flask, send_from_directory
from flask_restful import Api

from database_api import WealthApiHandler

app = Flask("app", static_folder='frontend/build')
api = Api(app)


@app.route("/")
def serve():
    return send_from_directory(app.static_folder, 'index.html')


api.add_resource(WealthApiHandler, '/wealth')
