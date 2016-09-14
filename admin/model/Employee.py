# coding:utf8
from mongoengine import *
from datetime import *
from django.db import models
from django.conf import settings # import the settings file
class Employee(Document):
    #meta = {'collection': settings.MONGODB_PREFIX+'user'}
    name = StringField(max_length=200, required=True)
    age = StringField()
    category = IntField()
    title = StringField()
    rating = StringField()
    created = DateTimeField()
    '''
    meta = {
        'indexes': [
            'title',
            '$title',  # text index
            '#title',  # hashed index
            ('title', '-rating'),
            ('category', '_cls'),
            {
                'fields': ['created'],
                'expireAfterSeconds': 3600
            }
        ]
    }
    '''
    