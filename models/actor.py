import datetime
from db import db

def validation(field):
    if not field:
        raise db.ValidationError("is missing")

class Actors(db.Document):
    meta = {'collection': 'actors', 'indexes': ['name']}
    name = db.StringField(required=True, unique=False, validation=validation)
    about = db.StringField(required=True, validation=validation)
    gender = db.StringField(required=True, validation=validation)
    avatar = db.DictField()
    createdAt = db.DateTimeField(required=True, default=datetime.datetime.utcnow)
    updatedAt = db.DateTimeField(required=True, default=datetime.datetime.utcnow)