# -*- coding: utf-8 -*-

from admin.controller.common_import import *  # 公共引入文件

from admin.model.User import User as Model

def _login(param):
    try:
        model = Model.objects.get(**param)
        if model:
            data = {
                'password': model['password'],
                'openId': model['openId'],
            }
            returnData = {'status': 200, 'msg': '成功', 'data': data}
        else:
            returnData = {'status': 700, 'msg': '失败', 'data': None}
    except Exception:
            returnData = {'code': 800, 'msg': '非法请求', 'data': None}

    return returnData

# 微信登录
@csrf_exempt
def wechat(request):
    post = request.POST
    unionId = post.get('unionId')
    openId = post.get('openId')
    param = {
        'unionId': unionId,
    }
    result = _login(param)
    if result.get('code') == 200 & result.get('data')['openId'] == openId:
        returnData = {'status': 200, 'msg': '成功', 'data': None}
    else:
        returnData = {'status': 900, 'msg': '失败', 'data': None}

    return HttpResponse(json.dumps(returnData))

# 用户名密码登录
@csrf_exempt
def userPwd(request):
    post = request.POST
    username = post.get('username')
    password = post.get('password')
    param = {
        'username': username,
    }
    result = _login(param)
    if result.get('code') == 200 & result.get('data')['password'] == password:
        returnData = {'status': 200, 'msg': '成功', 'data': None}
    else:
        returnData = {'status': 900, 'msg': '失败', 'data': None}

    return HttpResponse(json.dumps(returnData))