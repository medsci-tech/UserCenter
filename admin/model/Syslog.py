# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class Syslog(Auth):
    meta = Document.meta = {
        'collection': settings.MONGODB_PREFIX + 'syslog',
        'indexes': [],
    }
    createTime = DateTimeField(default=datetime.now())
    table = StringField()  # 操作的集合名
    tableId = StringField()  # 操作集合主键对应的id
    action = IntField()  # 动作
    actionName = StringField()  # 动作
    after = DictField()  # 操作后记录
    adminId = StringField()  # 操作用户id
    adminName = StringField()  # 操作用户
    ip = StringField()
