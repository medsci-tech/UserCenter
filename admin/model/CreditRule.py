# coding:utf8
from mongoengine import *
from datetime import *
from django.conf import settings  # import the settings file
from admin.model.Auth import Auth

class CreditRule(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'credit_rule',
            'indexes': [],
            }
    appId = StringField()
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    name = StringField()  # 策略名称
    credit = StringField()  # 扩展字段
    creditName = StringField()  # 扩展字段名称
    cycle = IntField(default=0)  # 周期
    cycleName = StringField()  # 周期名称 不要删
    rewardNum = IntField(default=0)  # 周期内最多奖励次数
    extends = DictField()
