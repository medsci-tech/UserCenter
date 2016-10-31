# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class Project(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'project',
            'indexes':['id'],
            }

    name_ch = StringField()  # 中文
    name_en = StringField()  # 英文

    company_id  = ObjectIdField()  # 企业id
    app_id      = ObjectIdField()  # 应用id

    contract_code   = StringField()  # 合同编号
    contract_rate   = FloatField()  # 比率
    contract_amount = FloatField()  # 合同金额
    contract_img    = StringField()

    used_beans  = IntField(default = 0)  # 已使用迈豆
    total_beans = IntField(default = 0)  # 已使用迈豆

    start_time  = StringField()
    end_time    = StringField()
    status      = IntField(default = 1)

    create_time = DateTimeField(default=datetime.now())
