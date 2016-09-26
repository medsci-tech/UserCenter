# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *


class CreditConfig(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'credit_config',
            'indexes': [],
            }
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    companyId = StringField()  # 策略名称
    appId = StringField()  # 应用
    appName = StringField()  # 扩展字段名称
    number = IntField(default=0)  # 周期
