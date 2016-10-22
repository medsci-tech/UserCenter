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

    companyId = StringField()  # 企业名称
    appId = StringField()  # 应用
    extend = DictField()  # 扩展
