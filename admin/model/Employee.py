# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

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
    