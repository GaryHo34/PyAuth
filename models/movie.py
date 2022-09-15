import datetime
from genres import GENRES
from typing_extensions import Required
from db import db


class Movie(db.Document):
    meta = {"collection": "movies"}
    title = db.StringField(required=True)
    storyLine = db.StringField(required=True)
    director = db.ReferenceField('actors')
    releasedDate = db.DateTimeField(required=True)
    status = db.StringField(required=True, choices=('public', 'private'))
    type = db.StringField(required=True)
    genres = db.ListField(db.StringField(choices=GENRES), required=True)
    tags = db.ListField(db.StringField(), required=True)
    cast = db.DictField(required=True)
    writers = db.ListField(db.ReferenceField('actors'))
    poster = db.DictField(required=True)
    trailer = db.DictField(required=True)
    reviews = db.ListField(db.ReferenceField('reviews')) 
    language = db.StringField(required=True)  
    createdAt = db.DateTimeField(
        required=True, default=datetime.datetime.utcnow)
    updatedAt = db.DateTimeField(
        required=True, default=datetime.datetime.utcnow)