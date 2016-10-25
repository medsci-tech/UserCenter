# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class Contract(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'contract',
            'indexes':['id'],
            }
    createTime = DateTimeField(default=datetime.now())

    companyId = StringField()  # 企业id
    appId = StringField()  # 应用id
    name = StringField()
    apiName = StringField()  #英文
    code = StringField()
    number = FloatField()
    extend = DictField()  # 扩展
    useBeans = IntField(default=0)  # 已使用迈豆
    totalBeans = IntField(default=0)  # 已使用迈豆
    amount = FloatField()
    img = StringField()
    startTime = StringField()
    endTime = StringField()
    status = IntField(default=1)
