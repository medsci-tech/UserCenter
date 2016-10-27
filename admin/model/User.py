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

    openid = StringField(default=None)
    unionid = StringField(default=None)
    password = StringField(max_length=100)  # 密码
    longitude = StringField(required=False)  # 经度
    latitude = StringField(required=False)  # 纬度
    phone = StringField()  # 手机号

    role = StringField(default=None)  # 角色
    beansList = DictField()  # 迈豆记录
    beans_total = FloatField(default=0)
    province = StringField(default=None)
    city = StringField(default=None)
    district = StringField(default=None)

# 用户表

    old_id = IntField(default=None)
    level_id = IntField(default=None)
    referrer_id = IntField(default=None)
    cooperator_id = IntField(default=None)
    is_registered = IntField(default=None)

    # phone = StringField(default=None)
    auth_code = StringField(default=None)
    auth_code_expired = StringField(default=None)
    nickname = StringField(default=None)
    head_image_url = StringField(default=None)
    qr_code = StringField(default=None)
    created_at = StringField(default=None)
    updated_at = StringField(default=None)

# 用户信息表
    type = StringField(default=None)
    level = IntField(default=None)
    name = StringField(default=None)
    referred_name = StringField(default=None)
    referred_phone = StringField(default=None)
    region = StringField(default=None)
    region_level = StringField(default=None)
    responsible = StringField(default=None)
    hospital = StringField(default=None)
    hospital_level = StringField(default=None)
    department = StringField(default=None)
    remark = StringField(default=None)

