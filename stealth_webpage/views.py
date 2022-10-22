# Todo:
# POST: 
#   /categories
#
# GET:
#   /categories
#

from flask import abort, jsonify, request
from stealth_webpage import app

categories = []
users = [{"id": 0, "name": "admin"}]

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
    