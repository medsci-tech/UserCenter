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
    cid = StringField()
    name = StringField()
    code = StringField()
    number = StringField()
    amount = StringField()
    img = StringField()
    startTime = StringField()
    endTime = StringField()
