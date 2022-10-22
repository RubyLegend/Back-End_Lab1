# Todo:
# POST: 
#   /categories
#
# GET:
#   /categories
#

import json
from flask import abort, jsonify, request
from stealth_webpage import app

categories = []

@app.route("/categories", methods=['GET', 'POST'])
def retrieve_categories():
    if request.method == 'GET':
        deserialized = []
        for element in categories:
            deserialized.append(json.loads(element))

        return jsonify({"categories": deserialized})
    else:
        data = dict(request.get_json())  # type: ignore
        if len(data) == 2 and 'id' in data and 'name' in data:
            categories.append(json.dumps(data))
            return jsonify({"success": "Ok", "data": data})
        elif len(data) == 1 and 'name' in data:
            data['id'] = json.loads(categories[len(categories)-1])['id']+1 # Getting id of last record and incrementing it
            categories.append(json.dumps(data))
            return jsonify({"success": "Ok", "data": data})
        else:
            abort(400)