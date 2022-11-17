from flask.views import MethodView
from flask import request, abort, jsonify
from flask_smorest import Blueprint

from stealthwebpage.logic import check_if_value_is_present
from stealthwebpage.db import users

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/users/<int:user_id>")
class UserActions(MethodView):
    def get(self, user_id):
        try:
            return users[user_id]
        except KeyError:
            abort(400, "User not found")
    
    def delete(self, user_id):
        try:
            deleted = users[user_id]
            del users[user_id]
            abort(200, "Ok. Removed " + str(jsonify(deleted)))
        except KeyError:
            abort(400, "User not found")

@blp.route("/users")
class UsersList(MethodView):
    def get(self):
        return jsonify({"users": users})
    
    def post(self):
        data = dict(request.get_json())  # type: ignore
        # Two parameters passed
        if len(data) == 2 and 'id' in data and 'name' in data:
            # Check if id is already claimed
            if check_if_value_is_present(users, 'id', data['id']):
                abort(400, "User ID already claimed.")
            # If not - append data.
            users.append(data)
            return jsonify({"success": "Ok", "data": data})
        # One parameter passed
        elif len(data) == 1 and 'name' in data:
            # If there is no data - set id to 0.
            if len(users) == 0:
                data['id'] = 1
            # Else auto-increment id
            else:
                data['id'] = users[-1]['id']+1 # Getting id of last record and incrementing it
            # Append data
            users.append(data)
            return jsonify({"success": "Ok", "data": data})

        # If no params passed, or there is more than needed - call error
        else:
            abort(400) 

