# coding:utf8
from mongoengine import *
from datetime import *
import bson

class Employee(Document):
    name = StringField()
    age = StringField()