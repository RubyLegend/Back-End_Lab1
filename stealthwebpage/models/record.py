from sqlalchemy import func
import sqlalchemy as sa
from stealthwebpage.db import db

class RecordModel(db.Model): # type: ignore
    __tablename__ = "records"

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, 
                        sa.ForeignKey("users.id"), 
                        unique=False, 
                        nullable=False)
    category_id = sa.Column(sa.Integer, 
                        sa.ForeignKey("categories.id"), 
                        unique=False, 
                        nullable=False)
    datetime = sa.Column(sa.TIMESTAMP, 
                         server_default=func.now())
    total = sa.Column(sa.Float(precision=2), 
                      unique=False, 
                      nullable=False)
    
    @property
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "datetime": self.datetime,
            "total": self.total
        }