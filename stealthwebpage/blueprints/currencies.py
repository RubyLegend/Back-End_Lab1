from flask_jwt_extended import jwt_required

from flask.views import MethodView
from flask import jsonify
from flask_smorest import abort, Blueprint

from stealthwebpage.schemas import CurrencySchema

from sqlalchemy.exc import IntegrityError
from stealthwebpage.models.currency import CurrencyModel
from stealthwebpage.db import db

blp = Blueprint("currency", __name__, description="Operations on currencies")


@blp.route("/currencies/<int:user_id>")
class CurrencyActions(MethodView):
    @blp.response(200,CurrencySchema)
    @blp.response(404,description="Currency not found")
    def get(self, currency_id):
        result = CurrencyModel.query.get_or_404(currency_id)
        return jsonify({"status": "OK", "result": result.serialize})
    
    @blp.response(200,CurrencySchema)
    @blp.response(404,description="Currency not found")
    @jwt_required()
    def delete(self, currency_id):
        currency = CurrencyModel.query.get_or_404(currency_id)
        currency_data = currency.serialize
        db.session.delete(currency)
        db.session.commit()
        return jsonify({"message": "Ok. Removed.", "data": currency_data})

@blp.route("/currencies")
class CurrenciesList(MethodView):
    @blp.response(200,CurrencySchema(many=True))
    def get(self):
        return CurrencyModel.query.all()
    
    @blp.arguments(CurrencySchema)
    @blp.response(200,CurrencySchema)
    @jwt_required
    def post(self, currency_data):
        currency = CurrencyModel(**currency_data)
        try:
            db.session.add(currency)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Currency with this name already exists")
        return jsonify({"status": "Ok", "data": currency_data})
