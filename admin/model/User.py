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

    unionId = StringField()  # 微信唯一标识
    username = StringField()  # 用户名
    phone = StringField()  # 手机号
    password = StringField()  # 密码
    role = IntField(default=0)  # 角色
    extend = DictField()  # 扩展

# 导入的字段

    _id = ObjectIdField(default=None)
    id = IntField(default=None)
    old_id = IntField(default=None)
    type_id = IntField(default=None)
    level_id = IntField(default=None)
    referrer_id = IntField(default=None)
    cooperator_id = IntField(default=None)
    is_registered = IntField(default=None)

    # phone = StringField(default=None)
    auth_code = StringField(default=None)
    auth_code_expired = StringField(default=None)
    beans_total = FloatField(default=None)
    openid = StringField(default=None)
    unionid = StringField(default=None)
    nickname = StringField(default=None)
    head_image_url = StringField(default=None)
    qr_code = StringField(default=None)
    created_at = StringField(default=None)
    updated_at = StringField(default=None)
