# coding:utf8
from mongoengine import *
from datetime import *
from django.db import models
from admin.model import Base
from django.conf import settings # import the settings file
class Employee(Base):
    meta = {'collection': settings.MONGODB_PREFIX+'admin'}
    composition             =   ListField()
    name = StringField(max_length=200, required=True)
    age = StringField()
    