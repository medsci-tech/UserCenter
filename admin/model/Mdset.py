# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class Mdset(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'mdset',
            'indexes': [],
            }
    appId = StringField()
    appName = StringField()  # 不要删
    ratio = FloatField(default=0)
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删
