# -*- coding: utf-8 -*-
# token 加密方法
from UserCenter.global_templates import configParam
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from django.http import HttpResponse
import time
import datetime
class QXToken(object):
    def __init__(self, name):
        self.name = name
        c_token = configParam().get('c_token')
        self.token_key = c_token['key']
        self.token_expire = c_token['expire']


    def generate_auth_token(self):
        ticks = int(time.time())  # 当前时间戳
        now = datetime.datetime.now()  # 获得当前时间
        otherStyleTime = now.strftime("%Y-%m-%d")  # 转换为指定的格式:
        endTime = otherStyleTime + ' 23:59:59'
        timeArray = time.strptime(endTime, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))  # 转换为时间戳
        expiration = timeStamp - ticks # 设置当天有效期
        s = Serializer(self.token_key, expires_in=expiration)
        return str(s.dumps({'name': self.name}), encoding="utf-8")

    def verify_auth_token(self, token):
        s = Serializer(self.token_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return 0 # valid token, but expired
        except BadSignature:
            return 0 # invalid token
        if data['name'] == self.name:
            return 200
            #return self.name
        else:
            return 0