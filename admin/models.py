# coding:utf8
from UserCenter.settings import DB_usercenter
from mongoengine import *

class User(Document):
    tables = DB_usercenter.md_user  # 获得表
    name = StringField()
    likes = StringField()
    def find(self,**kwargs):
        return  self.tables.find(kwargs)

    def add(self,**kwargs):
        return self.tables.insert(kwargs)
