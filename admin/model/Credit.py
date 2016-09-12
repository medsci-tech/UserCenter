# coding:utf8
from mongoengine import *
from datetime import *
from django.conf import settings  # import the settings file
from admin.model.Auth import Auth

class Credit(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'credit',
            'indexes': [],
            }
    appId = StringField()
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    credit = StringField()  # 扩展字段
    name = StringField()  # 扩展名称
    icon = StringField()  # 初始积分
    initNum = FloatField(default=0)  # 初始值
    ratio = FloatField(default=0)  # 兑换比例