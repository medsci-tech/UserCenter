# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class Contract(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'contract',
            'indexes':['id'],
            }
    companyId = StringField()  # 企业id
    appId = StringField()  # 应用id
    name = StringField()
    apiName = StringField()  #英文
    code = StringField()
    number = FloatField()
    extend = DictField()  # 扩展
    credit1 = IntField(default=0)  # 已分配迈豆列表
    amount = FloatField()
    img = StringField()
    startTime = StringField()
    endTime = StringField()
    status = IntField(default=1)
