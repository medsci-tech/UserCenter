# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class Credit(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'credit',
            'indexes': [],
            }
    appId = StringField()
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    credit = StringField()  # 扩展字段
    creditName = StringField()  # 扩展字段名称
    name = StringField()  # 扩展名称
    icon = StringField()  # 初始积分
    initNum = FloatField(default=0)  # 初始值
    ratio = FloatField(default=0)  # 兑换比例
