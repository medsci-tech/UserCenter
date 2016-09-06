# coding:utf8

from mongoengine import *
from datetime import *
from django.conf import settings
from admin.model.Auth import Auth

class App(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'app',
            'indexes': [],
            }
    name = StringField(required=True)
    description = StringField()
    status = IntField(default=1)
    statusName = StringField()  # 不要删
    createTime = DateTimeField(default=datetime.now())
