# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class BeanLog(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'bean_log',
            'indexes': [],
            }
    mysql_user_id = IntField(default=None)

    company_id      = ObjectIdField()
    company_name    = StringField()
    app_id          = ObjectIdField()
    app_name        = StringField()
    project_id      = ObjectIdField()
    project_name    = StringField()

    rule_id         = ObjectIdField()
    rule_name_ch    = StringField()
    rule_name_en    = StringField()
    rule_type_id    = ObjectIdField()
    rule_type_name  = StringField()

    user_id     = ObjectIdField()
    user_phone  = StringField()

    post_beans = IntField(default = 0)  # 迈豆参数值
    save_beans = IntField(default = 0)  # 迈豆参数经规则计算后的值

    create_time = DateTimeField(default = datetime.now())
