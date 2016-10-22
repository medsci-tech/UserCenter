# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class CreditLog(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'credit_log',
            'indexes': [],
            }
    createTime = DateTimeField(default=datetime.now())
    contractId = StringField()
    appId = StringField()
    credit1 = FloatField(default=0)  # 已分配迈豆列表
