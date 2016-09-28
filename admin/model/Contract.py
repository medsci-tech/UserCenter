# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

class Contract(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'contract',
            'indexes':['id'],
            }
    cid = StringField()
    name = StringField()
    code = StringField()
    number = StringField()
    amount = StringField()
    img = StringField()
    startTime = StringField()
    endTime = StringField()
    status = IntField(default=1)
