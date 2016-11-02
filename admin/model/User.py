# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class User(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'user',
            'indexes': [],
            }

    mysql_id            = IntField(default=None)  # 没用的id
    mysql_referrer_id   = IntField(default = None)

    phone       = StringField()  # 手机号
    password    = StringField()  # 密码
    role        = StringField(default=None)  # 角色

    province    = StringField(default = None)
    city        = StringField(default = None)
    district    = StringField(default = None)
    longitude   = StringField(required = False)  # 经度
    latitude    = StringField(required = False)  # 纬度

    beans_total = IntField(default = 0)
    beans_list  = DictField()

    # 推荐人
    referrer_id = IntField(default = None)
    referrer_name = StringField(default = None)
    referrer_phone = StringField(default = None)

    # doctors only
    region          = StringField(default = None)  # 医生大区
    region_level    = StringField(default = None)  # 大区级别
    region_admin    = StringField(default = None)  # 大区负责人
    hospital        = StringField(default = None)  # 医院
    hospital_level  = StringField(default = None)  # 医院等级
    department      = StringField(default = None)  # 科室

    created_at = StringField(default = datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at = StringField(default = None)
