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
from stealthwebpage.blueprints.currencies import blp as CurrencyBlueprint

from stealthwebpage.db import db
from stealthwebpage.models.currency import CurrencyModel
from sqlalchemy.exc import IntegrityError

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

with app.app_context():
    # IDK why, but this code executes twice, so in case of second execution
    # database will drop IntegrityError, which I'll simply skip
    try:
        # Inserting default value in table "Currency"
        currency_default_data = CurrencyModel(name='Hryvnia')
        db.session.add(currency_default_data)
        db.session.commit()
    except IntegrityError:
        pass
    
# Enforcing foreign key constraints
def _fk_pragma_on_connect(dbapi_con, con_record):
   dbapi_con.execute('pragma foreign_keys=ON')
with app.app_context():
   from sqlalchemy import event
   event.listen(db.engine, 'connect', _fk_pragma_on_connect)

api.register_blueprint(UserBlueprint)
api.register_blueprint(CategoriesBlueprint)
api.register_blueprint(RecordsBlueprint)
api.register_blueprint(CurrencyBlueprint)

@app.route("/", methods=['GET'])
def main():
    return """
            <h1>Welcome to the main page</h1>
            <br/>
            <p>To test this website, use this endpoints:</p>
            <ul>
                <li>/categories (GET, POST, DELETE)</li>
                <li>/users (GET, POST, DELETE)</li>
                <li>/currencies (GET, POST, DELETE)</li>
                <li>/records (GET, POST)</li>
                <li>/swagger-ui</li>
            </ul>
            <br/>
           """