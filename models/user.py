import datetime
from db import db


def name_validation(name):
    if not name:
        raise db.ValidationError("name is missing")


def password_validation(password):
    if not password:
        raise db.ValidationError("password is missing")

    if len(password) < 8 or len(password) > 20:
        raise db.ValidationError("password is too long")


class Users(db.Document):
    meta = {"collection": "users"}
    name = db.StringField(required=True,
                          unique=False,
                          validation=name_validation)
    email = db.EmailField(required=True)
    password = db.StringField(required=True,
                              validation=name_validation)
    isVerified = db.BooleanField(required=True, default=False)
    role = db.StringField(choices=('user', 'admin'), required=True, default='user')


class EmailToken(db.Document):
    meta = {
        'collection': 'emailtokens',
        'indexes': [
            {'fields': ['createAt'], 'expireAfterSeconds': 3600}
        ]
    }
    owner = db.ReferenceField('Users', required=True)
    token = db.StringField(required=True)
    createAt = db.DateTimeField(
        default=datetime.datetime.utcnow(), required=True)


class PasswordToken(db.Document):
    meta = {
        'collection': 'passwordtokens',
        'indexes': [
            {'fields': ['createAt'], 'expireAfterSeconds': 3600}
        ]
    }
    owner = db.ReferenceField('Users', required=True)
    token = db.StringField(required=True)
    createAt = db.DateTimeField(
        default=datetime.datetime.utcnow(), required=True)
