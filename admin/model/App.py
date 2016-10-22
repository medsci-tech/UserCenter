# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class App(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'app',
            'indexes': [],
            }
    name = StringField(required=True)
    companyId = StringField(required=True)
    description = StringField()
    status = IntField(default=1)
    createTime = DateTimeField(default=datetime.now())
