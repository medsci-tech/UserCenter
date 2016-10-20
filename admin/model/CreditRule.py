# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class CreditRule(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'credit_rule',
            'indexes': [],
            }
    appId = StringField()
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)

    name = StringField()  # 策略字段
    remark = StringField()  # 策略名称
    cycle = IntField(default=0)  # 周期
    rewardNum = IntField(default=0)  # 周期内最多奖励次数
    extend = DictField()
