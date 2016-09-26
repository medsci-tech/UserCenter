# coding:utf8
from django.conf import settings # import the settings file
from admin.model.Auth import Auth
from mongoengine import *
from datetime import *
import bson

class Contract(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'contract',
            'indexes':['id'],
            }
    id = StringField()
    name = StringField()
    code = StringField()
    number = StringField()
    amount = StringField()
    img = StringField()
    startTime = StringField()
    endTime = StringField()

    # 查询
    def find(self, **kwargs):
        return self.tables.find(kwargs)

    # 添加
    def add(self, **kwargs):
        kwargs.update(createTime=datetime.now())
        return self.tables.insert(kwargs)

    # 修改
    def editById(self, **kwargs):
        return self.tables.update({"id":kwargs.get('id')},{'$set':kwargs})


    # 批量修改
    def editByIds(self, selection, **kwargs):
        return self.tables.update({'id':{'$in':selection}},{'$set':kwargs},False,True,True)