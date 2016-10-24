# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *


class IntegralType(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'integral_type',
            'indexes': [],
            }
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)

    name = StringField()  # 名称
