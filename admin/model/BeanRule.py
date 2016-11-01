# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class BeanRule(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'bean_rule',
            'indexes': [],
            }

    name_ch     = StringField()  # 策略名称中文
    name_en     = StringField()  # 策略名称英文
    bean_type_id   = ObjectIdField()  # 策略类型
    bean_type_name   = StringField()  # 策略类型
    ratio       = FloatField()

    cycle   = IntField(default = 0)  # 周期
    limit   = IntField(default = 0)  # 周期内最多奖励次数
    status  = IntField(default = 1)

    company_id  = ObjectIdField()
    app_id      = ObjectIdField()
    project_id  = ObjectIdField()

    create_time = DateTimeField(default = datetime.now())

