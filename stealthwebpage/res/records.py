from datetime import datetime

from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.logic import check_if_value_is_present
from stealthwebpage.db import records, users, categories
from stealthwebpage.schemas import RecordSchema, RecordsQuerySchema

blp = Blueprint("records", __name__, description="Operations on records")

@blp.route("/records")
class RecordsList(MethodView):
    @blp.arguments(RecordsQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, RecordSchema(many=True), description="If no query args supplied")
    @blp.response(400, description="Only if no valid arguments were supplied as query params")
    def get(self, **kwargs):
        # If there is no query arguments - output all records
        if len(kwargs) == 0:
            return jsonify({"records": records})

        # Else parse arguments
        else:
            user = int(-1)
            category = int(-1)
            # Check for users
            if 'user' in kwargs:
                user = int(kwargs['user'])
            # Check for category
            if 'category' in kwargs:
                category = int(kwargs['category'])

            # Handle params based on supplied args
            if user != -1:
                if category != -1:
                    return get_records_per_user_and_category(user, category)
                return get_records_per_user(user)

            abort(400, message="No valid arguments supplied.")

    @blp.arguments(RecordSchema)
    @blp.response(200, RecordSchema)
    def post(self, record_data):
        # data = dict(request.get_json())  # type: ignore
        # Check if user exists
        if check_if_value_is_present(users, 'id', record_data['user_id']) == False:
            abort(400, message="This user doesn't exists.")

        # Check if catefory exists
        if check_if_value_is_present(categories, 'id', record_data['category_id']) == False:
            abort(400, message="This category doesn't exists.")

        # Auto increment id
        if len(records) == 0:
            record_data['id'] = 1
        else:
            record_data['id'] = records[-1]['id']+1 # Getting id of last record and incrementing it

        # Check for date
        if 'datetime' not in record_data:
            record_data['datetime'] = datetime.now()

        # Push new record_data
        records.append(record_data)
        return jsonify({"success": "Ok", "data": record_data})


@blp.route("/records/<int:user>")
@blp.response(200, description="Available records for selected user")
def get_records_per_user(user):
    ret = []
    for el in records:
        if el['user_id'] == user:
            ret.append(el)
    
    return jsonify({"user":user, "records": ret})

# Export records, which are belongs to user and to specific category
@blp.route("/records/<int:user>/<int:category>")
@blp.response(200, description="Available records for selected user in some category")
def get_records_per_user_and_category(user, category):
    ret = []
    for el in records:
        if el['user_id'] == user and el['category_id'] == category:
            ret.append(el)
    
    return jsonify({"user":user, "category": category, "records": ret})

