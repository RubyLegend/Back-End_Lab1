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
from stealthwebpage import app
from stealthwebpage.logic import check_if_value_is_present
import sys

categories = [{"id": 0, "name": "test_category"}]
users = [{"id": 0, "name": "admin"}]
records = [
        {
            "id":0,
            "userId": 0,
            "categoryId": 0,
            "date_time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "total": (int)(random()*1000)
        }
]

@app.route("/categories", methods=['GET'])
def retrieve_categories():
    return jsonify({"categories": categories})

@app.route("/categories", methods=['POST'])
def create_categories():
    data = dict(request.get_json())  # type: ignore
    if len(data) == 2 and 'id' in data and 'name' in data:
        if check_if_value_is_present(categories, 'id', data['id']):
            abort(400, "Category ID already claimed.")
        categories.append(data)
        return jsonify({"success": "Ok", "data": data})
    elif len(data) == 1 and 'name' in data:
        if len(categories) == 0:
            data['id'] = 1
        else:
            data['id'] = categories[len(categories)-1]['id']+1 # Getting id of last record and incrementing it
        categories.append(data)
        return jsonify({"success": "Ok", "data": data})
    else:
        abort(400) 

@app.route("/users", methods=['GET'])
def enumerate_user():
    return jsonify({"users": users})
    
@app.route("/users", methods=['POST'])
def create_user():
    data = dict(request.get_json())  # type: ignore
    if len(data) == 2 and 'id' in data and 'name' in data:
        if check_if_value_is_present(users, 'id', data['id']):
            abort(400, "User ID already claimed.")
        users.append(data)
        return jsonify({"success": "Ok", "data": data})
    elif len(data) == 1 and 'name' in data:
        data['id'] = users[len(users)-1]['id']+1 # Getting id of last record and incrementing it
        users.append(data)
        return jsonify({"success": "Ok", "data": data})
    else:
        abort(400) 
    
@app.route("/records", methods=['GET'])
def get_records():
    if len(request.args) == 0:
        return jsonify({"records": records})
    else:
        args = request.args.to_dict()
        user = int(-1)
        category = int(-1)
        if 'user' in args:
            user = int(args['user'])
        if 'category' in args:
            category = int(args['category'])
        if user != -1:
            if category != -1:
                return get_records_per_user_and_category(user, category)
            
            return get_records_per_user(user)

        abort(400, "No valid arguments supplied.")

@app.route("/records/<int:user>", methods=['GET'])
def get_records_per_user(user):
    ret = []
    for el in records:
        if el['userId'] == user:
            ret.append(el)
    
    return jsonify({"user":user, "records": ret})

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
    if len(data) == 5 and 'id' in data and 'userId' in data\
                      and 'categoryId' in data and 'date_time' in data and 'total' in data:
        if check_if_value_is_present(records, 'id', data['id']):
            abort(400, "Record ID already claimed.")
        if check_if_value_is_present(users, 'id', data['userId']) == False:
            abort(400, "This user doesn\'t exists.")
        if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
            abort(400, "This category doesn't exists.")
        data['date_time'] = datetime.strptime(data['date_time'], "%d-%m-%y %H:%M")
        records.append(data)
        return jsonify({"success": "Ok", "data": data})
    elif len(data) == 4 and 'userId' in data and 'categoryId' in data \
                        and 'date_time' in data and 'total' in data:
        if check_if_value_is_present(users, 'id', data['userId']) == False:
            abort(400, "This user doesn't exists.")
        if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
            abort(400, "This category doesn't exists.")
        data['id'] = users[len(users)-1]['id']+1 # Getting id of last record and incrementing it
        data['date_time'] = datetime.strptime(data['date_time'], "%d-%m-%y %H:%M")
        users.append(data)
        return jsonify({"success": "Ok", "data": data})
    elif len(data) == 3 and 'userId' in data and 'categoryId' in data \
                        and 'total' in data:
        if check_if_value_is_present(users, 'id', data['userId']) == False:
            abort(400, "This user doesn't exists.")
        if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
            abort(400, "This category doesn't exists.")
        data['id'] = users[len(users)-1]['id']+1 # Getting id of last record and incrementing it
        data['date_time'] = datetime.now().strftime("%d-%m-%y %H:%M")
        users.append(data)
        return jsonify({"success": "Ok", "data": data})
    else:
        abort(400) 