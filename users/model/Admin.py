# coding:utf8
from UserCenter.settings import DB_usercenter
from mongoengine import *
from datetime import *

class Admin(Document):
    tables = DB_usercenter.md_admin  # 获得表
    username = StringField()
    password = StringField()
    email = EmailField()
    status = IntField()

    # 查询
    def find(self,**kwargs):
        return  self.tables.find(kwargs)

    # 添加
    def add(self,**kwargs):
        kwargs.update(createTime=datetime.now())
        return self.tables.insert(kwargs)

