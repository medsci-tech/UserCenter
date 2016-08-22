# coding:utf8
from mongoengine import *
from datetime import *
import bson

class Admin(Document):
    tables = 'md_admin'  # 获得表
    username = StringField()
    nickname = StringField()
    password = StringField()
    email = EmailField()
    status = StringField()
    id = StringField()

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


    # 修改
    def editByFilter(self, selection, **kwargs):
        return self.tables.update({'id':{'$in':selection}},{'$set':kwargs},False,True,True)