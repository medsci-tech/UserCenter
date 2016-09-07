# coding:utf8
from mongoengine import *
from datetime import *
import bson
from django.conf import settings # import the settings file
from admin.model.Auth import Auth
from django_laravel_validator.validator import *
import bson
class Admin(Auth,Validator):
    meta = Document.meta = {
            'collection': settings.MONGODB_PREFIX+'admin',
            'indexes':[],
            }
    username = StringField(max_length=20, required=True,unique=True)
    nickname = StringField(max_length=20) 
    password = StringField()
    email = EmailField(max_length=20)
    createTime = DateTimeField(default=datetime.now())
    status = IntField(default=1)

    # 用户唯一验证数据
    def checkUsername(self, **kwargs):
        if Admin.objects(username=kwargs):
            response = {'status':0, 'msg': u'该用户已存在'}
            return kwargs
        else:
            return 1

    # email验证数据
    def checkEmail(self, **kwargs):
        if self.objects.filter(email=kwargs).exists():
            response = {'status': 0, 'msg': u'该email已存在'}
            return response

    def checkPasswor(self,**kwargs):
        if password1 and password2:
            if password1 != password2:
                response = {'status': 0, 'msg': u'两个密码字段不一致。'}
        return response
