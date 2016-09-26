# -*- coding: utf-8 -*-
# 公共引入文件
from admin.model.Common_import import *

import json
class Admin(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'admin',
            'indexes':[],
            }
    username = StringField(max_length=20, required=True,unique=True)
    nickname = StringField(max_length=20) 
    password = StringField()
    email = EmailField(max_length=20)
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)

    # 用户唯一验证数据
    def checkUsername(self, **kwargs):
        if Admin.objects.filter(username=kwargs):
            response = {'status':0, 'msg': u'该用户已存在!'}
            return json.dumps(response)
        else:
            response = {'status': 1, 'msg': None}
            return json.dumps(response)
