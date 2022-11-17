# Todo:
# POST: 
#   /categories
#   /users
#   /records
#
# GET:
#   /categories
#   /users
#   /records[/userId[/categoryId]]
#   /records[?user=userId[&category=categoryId]]
#

from datetime import datetime
from random import random
from tabnanny import check
from flask import abort, jsonify, request
from flask_smorest import Blueprint as blp
from flask_smorest import Api

from stealthwebpage import app
from stealthwebpage.logic import check_if_value_is_present
from stealthwebpage.db import *

from stealthwebpage.res.users import blp as UserBlueprint
from stealthwebpage.res.categories import blp as CategoriesBlueprint
from stealthwebpage.res.records import blp as RecordsBlueprint

app.config["PROPAGATE_EXCEPTION"] = True
app.config["API_TITLE"] = "Stealth Web Page"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(UserBlueprint)
api.register_blueprint(CategoriesBlueprint)
api.register_blueprint(RecordsBlueprint)

@app.route("/", methods=['GET'])
def main():
    return """
            <h1>Welcome to the main page</h1>
            <br/>
            <p>To test this website, use this endpoints:</p>
            <ul>
                <li>/categories (GET, POST)</li>
                <li>/users (GET, POST)</li>
                <li>/records (GET, POST)</li>
                <li>/swagger-ui</li>
            </ul>
            <br/>
           """