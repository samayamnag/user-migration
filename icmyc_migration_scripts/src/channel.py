from mongoengine.fields import (
    StringField, IntField, BooleanField,DateTimeField
)
from mongoengine import Document
import datetime


class Channel(Document):
    title = StringField(max_lenght=100, required=True)
    slug = StringField(max_lenght=150, required=True)
    platform = StringField(default="Swachhata", choices=['Swachhata', 'ICMYC'])
    app_name = StringField(required=True)
    type = StringField(required=True)
    archived = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()

    meta = {
        'collection': 'channels'
    }

    def __str__(self):
        return self.title
