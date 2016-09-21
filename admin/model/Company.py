# coding:utf8
from mongoengine import *
from datetime import *
from django.conf import settings  # import the settings file
from admin.model.Auth import Auth

class Company(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'company',
            'indexes': [],
            }
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    name = StringField()  # 策略名称
