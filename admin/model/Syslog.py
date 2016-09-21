# coding:utf8
from mongoengine import *
from datetime import *
from django.conf import settings  # import the settings file
from admin.model.Auth import Auth

class Syslog(Auth):
    meta = Document.meta = {
        'collection': settings.MONGODB_PREFIX + 'syslog',
        'indexes': [],
    }
    createTime = DateTimeField(default=datetime.now())
    table = StringField()  # 操作的集合名
    tableId = StringField()  # 操作集合主键对应的id
    action = IntField()  # 动作
    # actionName = StringField()  # 动作
    # after = DictField()  # 操作后记录
    # adminId = StringField()  # 操作用户id
    # adminName = StringField()  # 操作用户
    # ip = StringField()
