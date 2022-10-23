# Todo:
# POST: 
#   /categories
#
# GET:
#   /categories
#

from datetime import datetime
from random import random
from flask import abort, jsonify, request
from stealth_webpage import app

categories = [{"id": 0, "name": "test_category"}]
users = [{"id": 0, "name": "admin"}]
records = [
        {
            "id":0,
            "userId": 0,
            "categoryId": 0,
            "date_time": datetime.now().strftime("%d/%m/%y %H:%M"),
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
    return jsonify({"records": records})

@app.route("/records", methods=['POST'])
def create_record():
    data = dict(request.get_json())  # type: ignore
    if len(data) == 5 and 'id' in data and 'userId' in data\
                      and 'categoryId' in data and 'date_time' in data and 'total' in data:
        data['date_time'] = datetime.strptime(data['date_time'], "%d/%m/%y %H:%M")
        records.append(data)
        return jsonify({"success": "Ok", "data": data})
    elif len(data) == 4 and 'userId' in data and 'categoryId' in data \
                        and 'date_time' in data and 'total' in data:
        data['id'] = users[len(users)-1]['id']+1 # Getting id of last record and incrementing it
        data['date_time'] = datetime.strptime(data['date_time'], "%d/%m/%y %H:%M")
        users.append(data)
        return jsonify({"success": "Ok", "data": data})
    elif len(data) == 3 and 'userId' in data and 'categoryId' in data \
                        and 'total' in data:
        data['id'] = users[len(users)-1]['id']+1 # Getting id of last record and incrementing it
        data['date_time'] = datetime.now()
        users.append(data)
        return jsonify({"success": "Ok", "data": data})
    else:
        abort(400) 