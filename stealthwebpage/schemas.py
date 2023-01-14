from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    password = fields.Str(required=True)
    currency_id = fields.Int(required=False)

class UserLogin(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class CurrencySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    datetime = fields.DateTime("%d-%m-%Y %H:%M", required=False)
    total = fields.Float(required=True)
    currency_id = fields.Int(required=False)

class RecordsQuerySchema(Schema):
    user = fields.Int(required=False)
    category = fields.Int(required=False)
