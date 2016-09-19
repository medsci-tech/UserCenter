# coding:utf8
from mongoengine import *
from datetime import *
from django.conf import settings  # import the settings file
from admin.model.Auth import Auth

class Logs(Auth):
    meta = Document.meta = {
        'collection': settings.MONGODB_PREFIX+'logs',
        'indexes': [],
    }
    createTime = DateTimeField(default=datetime.now())
    table = StringField()  # 操作的集合名
    tableId = StringField()  # 操作集合主键对应的id
    action = StringField()  # 动作
    actionName = StringField()  # 动作
    before = StringField()  # 操作前记录
    after = StringField()  # 操作后记录
    adminId = StringField()  # 操作用户id
    adminName = StringField()  # 操作用户
    ip = StringField()
