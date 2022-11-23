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

from flask_smorest import Api

from stealthwebpage import app

from stealthwebpage.blueprints.users import blp as UserBlueprint
from stealthwebpage.blueprints.categories import blp as CategoriesBlueprint
from stealthwebpage.blueprints.records import blp as RecordsBlueprint

from stealthwebpage.db import db

app.config["PROPAGATE_EXCEPTION"] = True
app.config["API_TITLE"] = "Stealth Web Page"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

api = Api(app)

with app.app_context():
    db.create_all()

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