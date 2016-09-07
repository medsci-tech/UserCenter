# coding:utf8
from mongoengine import *
from datetime import *
import bson
from django.conf import settings  # import the settings file
from admin.model.Auth import Auth

class Mdset(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'mdset',
            'indexes': [],
            }
    appId = StringField()
    appName = StringField()  # 不要删
    ratio = StringField(required=True)
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删
