# -*- coding: utf-8 -*-
# token 加密方法
from UserCenter.global_templates import configParam
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

class QXToken(object):
    def __init__(self, name):
        self.name = name
        c_token = configParam().get('c_token')
        self.token_key = c_token['key']
        self.token_expire = c_token['expire']

    def generate_auth_token(self, expiration=None):
        s = Serializer(self.token_key, expires_in=expiration)
        return str(s.dumps({'name': self.name}), encoding="utf-8")

    def verify_auth_token(self, token):
        s = Serializer(self.token_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        if data['name'] == self.name:
            return self.name
        else:
            return None