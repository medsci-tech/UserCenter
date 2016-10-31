# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class Syslog(Auth):
    meta = Document.meta = {
        'collection': settings.MONGODB_PREFIX + 'syslog',
        'indexes': [],
    }

    admin_id    = StringField()  # 操作用户id
    admin_name  = StringField()  # 操作用户
    admin_ip    = StringField()

    table       = StringField()  # 操作集合
    table_id    = StringField()  # 操作集合主键对应的id

    action  = IntField()    # 动作
    after   = DictField()   # 操作后记录

    create_time = DateTimeField(default=datetime.now())
