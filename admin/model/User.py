# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class User(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'user',
            'indexes': [],
            }
    created_at = StringField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = StringField(default=None)
    password = StringField(max_length=100)  # 密码
    longitude = StringField(required=False)  # 经度
    latitude = StringField(required=False)  # 纬度
    phone = StringField()  # 手机号
    role = StringField(default=None)  # 角色
    beansList = DictField()  # 迈豆记录
    beans_total = IntField(default=0)
    province = StringField(default=None)
    city = StringField(default=None)
    district = StringField(default=None)
    referrer_id = IntField(default=None)  # 推荐人
    referred_name = StringField(default=None)
    referred_phone = StringField(default=None)

    region = StringField(default=None)  # 医生大区
    region_level = StringField(default=None)
    responsible = StringField(default=None)  # 大区负责人
    hospital = StringField(default=None)  # 医院
    hospital_level = StringField(default=None)  # 医院等级
    department = StringField(default=None)  # 科室

