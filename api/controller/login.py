# -*- coding: utf-8 -*-
# -author-zhaiyu
from api.controller.common_import import *  # 公共引入文件

from admin.model.User import User as Model
from django.contrib.auth.hashers import check_password

def _login(param):
    try:
        model = Model.objects.get(**param)
        if model:
            data = {
                'password': model.password,
                'openid': model.openid,
            }
            returnData = {'code': 200, 'msg': '成功', 'data': data}
        else:
            returnData = {'code': 700, 'msg': '失败', 'data': None}
    except Exception:
            returnData = {'code': 800, 'msg': '非法请求', 'data': None}

    return returnData

# 微信登录
@csrf_exempt
def wechat(request):
    post = request.POST
    unionid = post.get('unionid')
    openid = post.get('openid')
    param = {
        'unionid': unionid,
    }
    result = _login(param)
    if result.get('code') == 200 :
        if result.get('data')['openid'] == openid:
            returnData = {'code': 200, 'msg': '成功', 'data': None}
        else:
            returnData = {'code': 910, 'msg': '失败', 'data': None}
    else:
        returnData = {'code': 900, 'msg': '失败', 'data': None}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

# 用户名密码登录
@csrf_exempt
def user_pwd(request):
    post = request.POST
    phone = post.get('phone')
    password = post.get('password')
    param = {
        'phone': phone,
    }
    result = _login(param)
    if result.get('code') == 200:
        result_pwd = result.get('data')['password']
        if check_password(password, result_pwd):
            returnData = {'code': 200, 'msg': '成功', 'data': None}
        else:
            returnData = {'code': 910, 'msg': '失败', 'data': None}
    else:
        returnData = {'code': 900, 'msg': '失败', 'data': None}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

# TEST
@csrf_exempt
def test(request):
    param = {
        'name':'zhaiyu',
        'phone':'123456',
    }
    token = QXToken(param)
    # res = token.generate_auth_token()
    res = token.verify_auth_token(
        'eyJhbGciOiJIUzI1NiIsImlhdCI6MTQ3NjI2MzA3OSwiZXhwIjoxNDc2MjY2Njc5fQ.eyJuYW1lIjp7InBob25lIjoiMTIzNDU2IiwibmFtZSI6InpoYWl5dSJ9fQ.IoWmPbuoBbCiDDE3F9wvFJWfn5CXokeFIE9-fdbaUUg'
    )
    return HttpResponse(res['name'])