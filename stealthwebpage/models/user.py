import sqlalchemy as sa
from stealthwebpage.db import db

class UserModel(db.Model): # type: ignore
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(128), unique=True, nullable=False)

    record = db.relationship("RecordModel", back_populates="user", lazy="dynamic")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }