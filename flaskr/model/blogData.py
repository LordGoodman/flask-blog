from mongoengine import Document, IntField, DateTimeField, StringField
from marshmallow import Schema, fields
from datetime import datetime as dt

class user(Document):
    id = StringField(primary_key=True)
    username = StringField()
    password = StringField()

class blog(Document):
    id = StringField(primary_key=True)
    authorId = StringField()
    created = DateTimeField(default=dt.now)
    title = StringField()
    body = StringField()

class userSchema(Schema):
    id = fields.String()
    username = fields.String()
    password = fields.String()

class blogSchema(Schema):
    id = fields.String()
    authorId = fields.String()
    created = fields.DateTime()
    title = fields.String()
    body = fields.String()