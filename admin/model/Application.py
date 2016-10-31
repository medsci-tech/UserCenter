# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class Application(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'application',
            'indexes': [],
            }
    name        = StringField(required = True)
    description = StringField()
    status      = IntField(default = 1)
    company_id  = ObjectIdField(required = True)
    create_time = DateTimeField(default = datetime.now())
