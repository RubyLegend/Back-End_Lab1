from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.logic import check_if_value_is_present
from stealthwebpage.db import users
from stealthwebpage.schemas import UserSchema

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/users/<int:user_id>")
class UserActions(MethodView):
    @blp.response(200,UserSchema)
    @blp.response(400,description="User not found")
    def get(self, user_id):
        try:
            return users[user_id]
        except IndexError:
            abort(400, message="User not found")
    
    @blp.response(200,UserSchema)
    @blp.response(400,description="User not found")
    def delete(self, user_id):
        try:
            deleted = users[user_id]
            del users[user_id]
            abort(200, message="Ok. Removed.\n" + str(jsonify(deleted)))
        except IndexError:
            abort(400, message="User not found")

@blp.route("/users")
class UsersList(MethodView):
    @blp.response(200,UserSchema(many=True))
    def get(self):
        return jsonify({"users": users})
    
    @blp.arguments(UserSchema)
    @blp.response(200,UserSchema)
    def post(self, user_data):
        # If there is no user_data - set id to 1.
        if len(users) == 0:
            user_data['id'] = 1
        # Else auto-increment id
        else:
            user_data['id'] = users[-1]['id']+1 # Getting id of last record and incrementing it
        # Append user_data
        users.append(user_data)
        return jsonify({"success": "Ok", "data": user_data})
