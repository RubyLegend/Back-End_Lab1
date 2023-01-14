import sqlalchemy as sa
from stealthwebpage.db import db

class UserModel(db.Model): # type: ignore
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), unique=True, nullable=False)
    password = sa.Column(sa.String(128), nullable=False)
    currency_id = sa.Column(sa.Integer, sa.ForeignKey("currencies.id"), unique=False, nullable=False, server_default="1")
    
    records_user = db.relationship("RecordModel", backref="user", lazy="dynamic")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
