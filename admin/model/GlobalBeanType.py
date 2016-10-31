# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.CommonImport import *


class GlobalBeanType(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX + 'global_bean_type',
            'indexes': [],
            }
    name_ch = StringField()  # 中文名称
    name_en = StringField()  # 英文名称
    status  = IntField(default = 1)
    createTime = DateTimeField(default = datetime.now())

