# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class Company(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'company',
            'indexes': [],
            }

    name    = StringField()  # 企业名称
    status  = IntField(default = 1)
    create_time = DateTimeField(default = datetime.now())
