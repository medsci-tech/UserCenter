# -*- coding: utf-8 -*-
# 函数
# zhaiyu
from urllib import parse, request
import json


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
        returnData = json.loads(res.read().decode())
    except:
        returnData = {'contract_code': 500, 'msg': 'post error', 'data': None}
    return returnData