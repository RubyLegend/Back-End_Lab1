from flask.views import MethodView
from flask import request, abort, jsonify
from flask_smorest import Blueprint

from stealthwebpage.logic import check_if_value_is_present
from stealthwebpage.db import categories

blp = Blueprint("categories", __name__, description="Operations on categories")

@blp.route("/catorigies/<int:category_id>")
class CategoryAction(MethodView):
    def get(self, category_id):
        try:
            return categories[category_id]
        except KeyError:
            abort(400, "Category not found")
    
    def delete(self, category_id):
        try:
            deleted_category = categories[category_id]
            del categories[category_id]
            abort(200, "Ok. Removed.\n" + str(jsonify(categories[category_id])))
        except KeyError:
            abort(400, "Category not found")

@blp.route("/categories")
class CategoriesList(MethodView):
    def get(self):
        return jsonify({"categories": categories})
    
    def post(self):
        data = dict(request.get_json())  # type: ignore
        # Two parameters passed
        if len(data) == 2 and 'id' in data and 'name' in data:
            # Check if id is already claimed
            if check_if_value_is_present(categories, 'id', data['id']):
                abort(400, "Category ID already claimed.")
            # If not - append data.
            categories.append(data)
            return jsonify({"success": "Ok", "data": data})
        # One parameter passed
        elif len(data) == 1 and 'name' in data:
            # If there is no data - set id to 0.
            if len(categories) == 0:
                data['id'] = 1
            # Else auto-increment id
            else:
                data['id'] = categories[-1]['id']+1 # Getting id of last record and incrementing it
            # Append data
            categories.append(data)
            return jsonify({"success": "Ok", "data": data})
        
        # If no params passed, or there is more than needed - call error
        else:
            abort(400) 

