from flask.views import MethodView
from flask import jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.schemas import UserSchema

from sqlalchemy.exc import IntegrityError
from stealthwebpage.models.user import UserModel
from stealthwebpage.db import db

blp = Blueprint("users", __name__, description="Operations on users")


@blp.route("/users/<int:user_id>")
class UserActions(MethodView):
    @blp.response(200,UserSchema)
    @blp.response(404,description="User not found")
    def get(self, user_id):
        result = UserModel.query.get_or_404(user_id)
        return jsonify({"status": "OK", "result": result.serialize})
    
    @blp.response(200,UserSchema)
    @blp.response(404,description="User not found")
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        user_data = user.serialize
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Ok. Removed.", "data": user_data})

@blp.route("/users")
class UsersList(MethodView):
    @blp.response(200,UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
    
    @blp.arguments(UserSchema)
    @blp.response(200,UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=["Some data failed validation.", e.args[0]])
        return jsonify({"status": "Ok", "data": user_data})
