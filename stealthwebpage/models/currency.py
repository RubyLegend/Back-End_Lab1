import sqlalchemy as sa
from stealthwebpage.db import db

class CurrencyModel(db.Model): # type: ignore
    __tablename__ = "currencies"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), unique=True, nullable=False)

    records_currency = db.relationship("RecordModel", backref="currency", lazy="dynamic")
    currency_user = db.relationship("UserModel", backref="currency", lazy="dynamic")
    
    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }