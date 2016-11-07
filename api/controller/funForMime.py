# -*- coding: utf-8 -*-
# 函数
# zhaiyu
from urllib import parse, request
import json
import time
import base64
import hashlib

# ===============
# 模拟post请求
# ===============
def imitate_post(**kwargs):
    url = kwargs.get('url')
    param = kwargs.get('param')  # 参数
    '''示例
    param = {
        'phone': '15623093771',
        'rule_name_en': 'follow_vendor',
        'app_id': '1',
        'mdBeans': '1',
        'token': 'eyJpYXQiOjE0Nzc0NTQ0NjQsImV4cCI6MTQ3NzQ5NzU5OSwiYWxnIjoiSFMyNTYifQ.eyJuYW1lIjoiNTgwYzA1YWU0ZWFhNzY1M2Y3MGQ4MmEzIn0.iMlxBuNtjfGJ2LWvkKilPagFnQv7WwWHKwNVxgJ9Rj4'
    }
    '''
    data = parse.urlencode(param)
    try:
        req = request.Request(url, data.encode(encoding='utf-8'))
        res = request.urlopen(req)
        return json.loads(res.read().decode())
    except:
        return {'code': 500, 'msg':'post error', 'data': None}



# ============================
# 文件解密
# ============================

def tcodes(strs, isEncrypt=1, key='mime.org.cn'):
    strs.encode('utf-8')
    now_time = time.time()
    dynKey = hashlib.new("sha1", str(now_time)).hexdigest() if isEncrypt == 1 else strs[0:40]
    dykey1 = dynKey[0:20].encode('utf-8')
    dykey2 = dynKey[20:].encode('utf-8')

    fixKey = hashlib.new("sha1", key.encode('utf-8')).hexdigest()
    fixkey1 = fixKey[0:20].encode('utf-8')
    fixkey2 = fixKey[20:].encode('utf-8')
    newkey = hashlib.new("sha1", dykey1 + fixkey1 + dykey2 + fixkey2).hexdigest()

    if (isEncrypt == 1):
        newstring = fixkey1 + strs + dykey2
    else:
        newstring = base64.b64decode(strs[40:].replace('_', '='))

    re = ''
    strlen = len(newstring)

    for i in range(0, strlen):
        j = i % 40
        re += chr(ord(chr(newstring[i])) ^ ord(newkey[j]))

    return dynKey + base64.b64encode(re).replace('=', '_') if isEncrypt == 1 else re[20:-20]

