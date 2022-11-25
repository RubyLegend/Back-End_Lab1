from datetime import datetime

from flask.views import MethodView
from flask import request, jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.schemas import RecordSchema, RecordsQuerySchema

from sqlalchemy.exc import IntegrityError
from stealthwebpage.models.record import RecordModel
from stealthwebpage.db import db

blp = Blueprint("records", __name__, description="Operations on records")

@blp.route("/records")
class RecordsList(MethodView):
    @blp.arguments(RecordsQuerySchema, location="query", as_kwargs=True)
    @blp.response(200, RecordSchema(many=True), description="If no query args supplied")
    @blp.response(400, description="If no valid arguments were supplied as query params")
    def get(self, **kwargs):
        # If there is no query arguments - output all records
        if len(kwargs) == 0:
            records = RecordModel.query.all()
            ret = [i.serialize for i in records]

            return ret


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
        record = RecordModel(**record_data)
        try:
            db.session.add(record)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Foreign key constraint failed.")
        return jsonify({"success": "Ok", "data": record.serialize})


@blp.route("/records/<int:user>")
@blp.response(200, description="Available records for selected user")
@blp.response(400, description="User not found")
def get_records_per_user(user):
    records = RecordModel.query.filter(RecordModel.user_id == user).all()
    ret = []
    for i in records:
        ret.append(i.serialize)
    
    return ret

# Export records, which are belongs to user and to specific category
@blp.route("/records/<int:user>/<int:category>")
@blp.response(200, description="Available records for selected user in some category")
@blp.response(400, description="User or category not found")
def get_records_per_user_and_category(user, category):
    records = RecordModel.query.filter(RecordModel.user_id == user, RecordModel.category_id == category).all()
    ret = []
    for i in records:
        ret.append(i.serialize)
    
    return ret

