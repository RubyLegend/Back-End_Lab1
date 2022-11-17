from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.logic import check_if_value_is_present
from stealthwebpage.db import categories
from stealthwebpage.schemas import CategorySchema

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/catorigies/<int:category_id>")
class CategoryAction(MethodView):
    def get(self, category_id):
        try:
            return categories[category_id]
        except IndexError:
            abort(400, message="Category not found")
    
    def delete(self, category_id):
        try:
            deleted_category = categories[category_id]
            del categories[category_id]
            abort(200, message="Ok. Removed.\n" + str(jsonify(categories[category_id])))
        except IndexError:
            abort(400, message="Category not found")

@blp.route("/categories")
class CategoriesList(MethodView):
    def get(self):
        return jsonify({"categories": categories})
    
    @blp.arguments(CategorySchema)
    def post(self, category_data):
        # data = dict(request.get_json())  # type: ignore
        # If there is no category_data - set id to 1.
        if len(categories) == 0:
            category_data['id'] = 1
        # Else auto-increment id
        else:
            category_data['id'] = categories[-1]['id']+1 # Getting id of last record and incrementing it
        # Append category_data
        categories.append(category_data)
        return jsonify({"success": "Ok", "data": category_data})


