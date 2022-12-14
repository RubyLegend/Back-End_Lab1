from stealthwebpage.db import db

class CategoryModel(db.Model): # type: ignore
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    records_category = db.relationship("RecordModel", backref="category", lazy="dynamic")

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }