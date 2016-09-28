# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class User(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'user',
            'indexes': [],
            }
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)
    statusName = StringField()  # 不要删

    unionId = StringField()  # 微信唯一标识
    username = StringField()  # 用户名
    phone = StringField()  # 手机号
    password = StringField()  # 密码
    role = IntField(default=0)  # 角色
    roleName = StringField()  # 角色
    extend = DictField()  # 扩展
