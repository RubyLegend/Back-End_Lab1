from passlib.hash import pbkdf2_sha256

from flask_jwt_extended import create_access_token

from flask.views import MethodView
from flask import jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.schemas import UserSchema, UserLogin

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
        user = UserModel(name=user_data["name"],
                         password=pbkdf2_sha256.hash(user_data["password"]))
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message=["Some data failed validation.", e.args[0]])
        return jsonify({"status": "Ok", "data": user_data})

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLogin)
    @blp.response(200, UserLogin)
    def post(self, user_data):
        user = UserModel.query.filter_by(name=user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id) 
            return jsonify({"status": "Ok", "access_token": access_token})

        return abort(400, message="User not found")
