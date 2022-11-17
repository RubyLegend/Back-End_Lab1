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

app.config["PROPAGATE_EXCEPTION"] = True
app.config["API_TITLE"] = "Stealth Web Page"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(UserBlueprint)


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
            </ul>
            <br/>
           """

@app.route("/categories", methods=['GET'])
def retrieve_categories():
    return jsonify({"categories": categories})

@app.route("/categories", methods=['POST'])
def create_categories():
    data = dict(request.get_json())  # type: ignore
    # Two parameters passed
    if len(data) == 2 and 'id' in data and 'name' in data:
        # Check if id is already claimed
        if check_if_value_is_present(categories, 'id', data['id']):
            abort(400, "Category ID already claimed.")
        # If not - append data.
        categories.append(data)
        return jsonify({"success": "Ok", "data": data})
    # One parameter passed
    elif len(data) == 1 and 'name' in data:
        # If there is no data - set id to 0.
        if len(categories) == 0:
            data['id'] = 1
        # Else auto-increment id
        else:
            data['id'] = categories[-1]['id']+1 # Getting id of last record and incrementing it
        # Append data
        categories.append(data)
        return jsonify({"success": "Ok", "data": data})
    
    # If no params passed, or there is more than needed - call error
    else:
        abort(400) 

# @app.route("/users", methods=['GET'])
# def enumerate_user():
#     return jsonify({"users": users})
    
# @app.route("/users", methods=['POST'])
# def create_user():
#     data = dict(request.get_json())  # type: ignore
#     # Two parameters passed
#     if len(data) == 2 and 'id' in data and 'name' in data:
#         # Check if id is already claimed
#         if check_if_value_is_present(users, 'id', data['id']):
#             abort(400, "User ID already claimed.")
#         # If not - append data.
#         users.append(data)
#         return jsonify({"success": "Ok", "data": data})
#     # One parameter passed
#     elif len(data) == 1 and 'name' in data:
#         # If there is no data - set id to 0.
#         if len(users) == 0:
#             data['id'] = 1
#         # Else auto-increment id
#         else:
#             data['id'] = users[-1]['id']+1 # Getting id of last record and incrementing it
#         # Append data
#         users.append(data)
#         return jsonify({"success": "Ok", "data": data})
    
#     # If no params passed, or there is more than needed - call error
#     else:
#         abort(400) 
    
@app.route("/records", methods=['GET'])
def get_records():
    # If there is no query arguments - output all records
    if len(request.args) == 0:
        return jsonify({"records": records})
    
    # Else parse arguments
    else:
        args = request.args.to_dict()
        user = int(-1)
        category = int(-1)
        # Check for users
        if 'user' in args:
            user = int(args['user'])
        # Check for category
        if 'category' in args:
            category = int(args['category'])
        
        # Handle params based on supplied args
        if user != -1:
            if category != -1:
                return get_records_per_user_and_category(user, category)
            return get_records_per_user(user)

        abort(400, "No valid arguments supplied.")

# Export records, which are belongs to user
@app.route("/records/<int:user>", methods=['GET'])
def get_records_per_user(user):
    ret = []
    for el in records:
        if el['userId'] == user:
            ret.append(el)
    
    return jsonify({"user":user, "records": ret})

# Export records, which are belongs to user and to specific category
@app.route("/records/<int:user>/<int:category>", methods=['GET'])
def get_records_per_user_and_category(user, category):
    ret = []
    for el in records:
        if el['userId'] == user and el['categoryId'] == category:
            ret.append(el)
    
    return jsonify({"user":user, "category": category, "records": ret})

@app.route("/records", methods=['POST'])
def create_record():
    data = dict(request.get_json())  # type: ignore
    # If there is 5 correct arguments supplied
    if len(data) == 5 and 'id' in data and 'userId' in data\
                      and 'categoryId' in data and 'date_time' in data and 'total' in data:
        # Check if values correct
        if check_if_value_is_present(records, 'id', data['id']):
            abort(400, "Record ID already claimed.")
        
        # Check if user exists
        if check_if_value_is_present(users, 'id', data['userId']) == False:
            abort(400, "This user doesn\'t exists.")

        # Check if catefory exists
        if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
            abort(400, "This category doesn't exists.")

        # Check for correct data format
        data['date_time'] = datetime.strptime(data['date_time'], "%d-%m-%y %H:%M")

        # Append data
        records.append(data)
        return jsonify({"success": "Ok", "data": data})
    
    # If there is 4 correct arguments supplied (ID not supplied)
    elif len(data) == 4 and 'userId' in data and 'categoryId' in data \
                        and 'date_time' in data and 'total' in data:
        # Check if user exists
        if check_if_value_is_present(users, 'id', data['userId']) == False:
            abort(400, "This user doesn't exists.")

        # Check if catefory exists
        if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
            abort(400, "This category doesn't exists.")
        
        # Auto increment id
        if len(records) == 0:
            data['id'] = 1
        else:
            data['id'] = records[-1]['id']+1 # Getting id of last record and incrementing it

        # Check for data format
        data['date_time'] = datetime.strptime(data['date_time'], "%d-%m-%y %H:%M")

        # Push new data
        records.append(data)
        return jsonify({"success": "Ok", "data": data})
    
    # If there is 3 arguments supplied (no ID and Date)
    elif len(data) == 3 and 'userId' in data and 'categoryId' in data \
                        and 'total' in data:
        # Check if user exists
        if check_if_value_is_present(users, 'id', data['userId']) == False:
            abort(400, "This user doesn't exists.")

        # Check if catefory exists
        if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
            abort(400, "This category doesn't exists.")
        
        # Auto increment id
        if len(records) == 0:
            data['id'] = 1
        else:
            data['id'] = records[-1]['id']+1 # Getting id of last record and incrementing it

        # Check for data format
        data['date_time'] = datetime.now().strftime("%d-%m-%y %H:%M")

        # Push new data
        records.append(data)
        return jsonify({"success": "Ok", "data": data})
    
    # Else if there is not enough arguments, or there is wrong count of it
    else:
        abort(400) 