# coding:utf8
from UserCenter.settings import DB_usercenter
from mongoengine import *
from datetime import *
import bson
from django.db.models import Q

class Admin(Document):
    tables = DB_usercenter.md_admin  # 获得表
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
    def editByFilter(self, **kwargs):
        # return self.tables.update({'id':{'$in':['1','6']}},{'$set':kwargs})
        return self.tables.update({'id':{'$in':['1','6']}},{'$set':kwargs},False,True,True)