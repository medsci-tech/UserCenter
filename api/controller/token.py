# -*- coding: utf-8 -*-
# token 加密方法
from UserCenter.global_templates import configParam
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

class QXToken(object):
    def __init__(self, name):
        self.name = name
        self.token_key = configParam().get('c_token_key')

    def generate_auth_token(self, expiration = 3600):
        s = Serializer(self.token_key, expires_in=expiration)
        return s.dumps({'name': self.name })

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