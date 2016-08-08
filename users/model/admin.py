# coding:utf8
from UserCenter.settings import DB_usercenter
from mongoengine import *

class Admin(Document):
    tables = DB_usercenter.md_admin  # 获得表
    username = StringField()
    password = StringField()
    email = StringField()
    status = IntField()
    createTime = DateTimeField()

    # 查询
    def find(self,**kwargs):
        return  self.tables.find(kwargs)

    # 添加
    def add(self,**kwargs):
        return self.tables.insert(kwargs)
