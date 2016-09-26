# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class Company(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'company',
            'indexes': [],
            }
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    name = StringField()  # 策略名称
