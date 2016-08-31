# coding:utf8
from mongoengine import *
from datetime import *
import bson
from django.conf import settings # import the settings file
from admin.model.Auth import Auth
class Mdset(Auth):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'mdset',
            'indexes':['_id'],
            }
    appId = StringField(required=True)
    ratio = StringField(max_length=20, required=True)
    status = StringField()
    _id = StringField(choices=(0,1))

    # 查询
    def find(self, **kwargs):
        return self.find(kwargs)

    # 添加
    def add(self, **kwargs):
        kwargs.update(createTime=datetime.now())
        return self.tables.insert(kwargs)

    # 修改
    def editById(self, **kwargs):
        return self.tables.update({"id":kwargs.get('id')},{'$set':kwargs})


    # 修改
    def editByFilter(self, selection, **kwargs):
        return self.tables.update({'id':{'$in':selection}},{'$set':kwargs},False,True,True)