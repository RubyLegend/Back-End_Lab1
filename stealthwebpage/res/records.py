from datetime import datetime

from flask.views import MethodView
from flask import request, abort, jsonify
from flask_smorest import Blueprint

from stealthwebpage.logic import check_if_value_is_present
from stealthwebpage.db import records, users, categories

blp = Blueprint("records", __name__, description="Operations on records")

@blp.route("/records")
class RecordsList(MethodView):
    def get(self):
        # If there is no query arguments - output all records
        if len(request.args) == 0:
            return jsonify({"records": records})

        # Else parse arguments
        else:
            args = request.args.to_dict()
            user = int(-1)
            category = int(-1)
            # Check for users
            if 'user' in args:
                user = int(args['user'])
            # Check for category
            if 'category' in args:
                category = int(args['category'])

            # Handle params based on supplied args
            if user != -1:
                if category != -1:
                    return get_records_per_user_and_category(user, category)
                return get_records_per_user(user)

            abort(400, "No valid arguments supplied.")
    def post(self):
        data = dict(request.get_json())  # type: ignore
        # If there is 5 correct arguments supplied
        if len(data) == 5 and 'id' in data and 'userId' in data\
                          and 'categoryId' in data and 'date_time' in data and 'total' in data:
            # Check if values correct
            if check_if_value_is_present(records, 'id', data['id']):
                abort(400, "Record ID already claimed.")

            # Check if user exists
            if check_if_value_is_present(users, 'id', data['userId']) == False:
                abort(400, "This user doesn\'t exists.")

            # Check if catefory exists
            if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
                abort(400, "This category doesn't exists.")

            # Check for correct data format
            data['date_time'] = datetime.strptime(data['date_time'], "%d-%m-%y %H:%M")

            # Append data
            records.append(data)
            return jsonify({"success": "Ok", "data": data})

        # If there is 4 correct arguments supplied (ID not supplied)
        elif len(data) == 4 and 'userId' in data and 'categoryId' in data \
                            and 'date_time' in data and 'total' in data:
            # Check if user exists
            if check_if_value_is_present(users, 'id', data['userId']) == False:
                abort(400, "This user doesn't exists.")

            # Check if catefory exists
            if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
                abort(400, "This category doesn't exists.")

            # Auto increment id
            if len(records) == 0:
                data['id'] = 1
            else:
                data['id'] = records[-1]['id']+1 # Getting id of last record and incrementing it

            # Check for data format
            data['date_time'] = datetime.strptime(data['date_time'], "%d-%m-%y %H:%M")

            # Push new data
            records.append(data)
            return jsonify({"success": "Ok", "data": data})

        # If there is 3 arguments supplied (no ID and Date)
        elif len(data) == 3 and 'userId' in data and 'categoryId' in data \
                            and 'total' in data:
            # Check if user exists
            if check_if_value_is_present(users, 'id', data['userId']) == False:
                abort(400, "This user doesn't exists.")

            # Check if catefory exists
            if check_if_value_is_present(categories, 'id', data['categoryId']) == False:
                abort(400, "This category doesn't exists.")

            # Auto increment id
            if len(records) == 0:
                data['id'] = 1
            else:
                data['id'] = records[-1]['id']+1 # Getting id of last record and incrementing it

            # Check for data format
            data['date_time'] = datetime.now().strftime("%d-%m-%y %H:%M")

            # Push new data
            records.append(data)
            return jsonify({"success": "Ok", "data": data})

        # Else if there is not enough arguments, or there is wrong count of it
        else:
            abort(400) 


@blp.route("/records/<int:user>")
def get_records_per_user(user):
    ret = []
    for el in records:
        if el['userId'] == user:
            ret.append(el)
    
    return jsonify({"user":user, "records": ret})

# Export records, which are belongs to user and to specific category
@blp.route("/records/<int:user>/<int:category>")
def get_records_per_user_and_category(user, category):
    ret = []
    for el in records:
        if el['userId'] == user and el['categoryId'] == category:
            ret.append(el)
    
    return jsonify({"user":user, "category": category, "records": ret})

