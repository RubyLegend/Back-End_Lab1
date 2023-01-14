from flask_jwt_extended import jwt_required

from flask.views import MethodView
from flask import jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.schemas import CategorySchema

from sqlalchemy.exc import IntegrityError
from stealthwebpage.models.category import CategoryModel
from stealthwebpage.db import db

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/categories/<int:category_id>")
class CategoryAction(MethodView):
    @blp.response(200,CategorySchema)
    @blp.response(404, description="Category not found")
    def get(self, category_id):
        result = CategoryModel.query.get_or_404(category_id)
        return jsonify({"status": "OK", "result": result.serialize})
    
    @blp.response(200,CategorySchema)
    @blp.response(404, description="Category not found")
    @jwt_required()
    def delete(self, category_id):
        user = CategoryModel.query.get_or_404(category_id)
        user_data = user.serialize
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Ok. Removed.", "data": user_data})

@blp.route("/categories")
class CategoriesList(MethodView):
    @blp.response(200,CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()
    
    @blp.arguments(CategorySchema)
    @blp.response(200, CategorySchema)
    @jwt_required()
    def post(self, category_data):
        category = CategoryModel(**category_data)
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Category with this name already exists")
        return jsonify({"status": "Ok", "data": category_data})


