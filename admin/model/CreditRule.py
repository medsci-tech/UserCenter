# coding:utf8
from mongoengine import *
from datetime import *
from django.conf import settings  # import the settings file
from admin.model.Auth import Auth

class CreditRule(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'credit_rule',
            'indexes': [],
            }
    appId = StringField()
    appName = StringField()  # 不要删
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    name = StringField()
    icon = StringField()
    initNum = IntField(default=0)
    ratio = IntField(default=0)
