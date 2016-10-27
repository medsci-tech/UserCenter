# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class BeansLog(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'api_beans_log',
            'indexes': [],
            }
    createTime = DateTimeField(default=datetime.now())

    appId = StringField()
    appName = StringField()
    companyId = StringField()
    companyName = StringField()
    contractId = StringField()
    contractName = StringField()
    ruleId = StringField()
    ruleName = StringField()

    phone = StringField()  # 手机号
    action = StringField()
    post_beans = IntField(default=0)  # 迈豆参数值
    save_beans = IntField(default=0)  # 迈豆参数经规则计算后的值
