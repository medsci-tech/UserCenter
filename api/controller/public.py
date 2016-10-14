# -*- coding: utf-8 -*-
'''
    公共访问方法

'''
from api.controller.common_import import *  # 公共引入文件

from admin.model.User import User as Model
from django.contrib.auth.hashers import check_password, make_password

# ============================
# 获取token
# ============================
@csrf_exempt
def get_token(request):
    post = request.POST
    if not post:
        returnData = {'code': 811, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    id = post.get('uc_uid')
    token = QXToken(id).generate_auth_token()
    returnData = {'code': 200, 'msg': '成功', 'data': token}
    return HttpResponse(json.dumps(returnData), content_type="application/json")

# ============================
# 查询单条数据私有方法
# ============================
def _getUser(param, data_param):
    try:
        model = Model.objects.get(**param)
    except Exception:
        return {'code': 800, 'msg': '非法请求', 'data': None}
    if model:
        data = {
            '%s' % data_param: model[data_param],
            'uc_uid': str(model['_id']),
        }
        returnData = {'code': 200, 'msg': '成功', 'data': data}
    else:
        returnData = {'code': 700, 'msg': '失败', 'data': None}
    return returnData

# ============================
# 用户登录
# ============================
@csrf_exempt
def login(request):
    post = request.POST
    if not post:
        returnData = {'code': 811, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    # 微信
    unionid = post.get('unionid')
    openid = post.get('openid')
    # 账号
    username = post.get('username')
    password = post.get('password')
    if unionid and openid:
        # 微信参数
        param = {
            'unionid': unionid,
        }
        data_param = 'openid'
        check_value = openid
    elif username and password:
        # 账号参数
        param = {
            'username': username,
        }
        data_param = 'password'
        check_value = password
    else:
        returnData = {'code': 811, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    result = _getUser(param, data_param)
    if result.get('code') == 200 :
        uc_uid = result.get('data')['uc_uid']
        if result.get('data')[data_param] == check_value:
            token = QXToken(uc_uid).generate_auth_token()
            returnData = {'code': 200, 'msg': '成功', 'data': {'uc_uid': uc_uid, 'token': token}}
        else:
            returnData = {'code': 910, 'msg': '失败', 'data': None}
    else:
        returnData = result

    return HttpResponse(json.dumps(returnData), content_type="application/json")

# ============================
# 插入数据私有方法
# ============================
def _addUser(param):
    username = param.get('username')
    unionid = param.get('unionid')
    if unionid:
        check_param = {
            'unionid': unionid,
        }
        data_param = 'unionid'
    elif username:
        check_param = {
            'username': username,
        }
        data_param = 'username'
    else:
        return {'code': 902, 'msg': '非法操作', 'data': None}
    check_exist = _getUser(check_param, data_param)
    if check_exist.get('code') == 200:
        return {'code': 901, 'msg': '用户已存在', 'data': None}
    try:
        model = Model.objects.create(**param)
    except Exception:
        return {'code': 900, 'msg': '数据验证错误', 'data': None}
    if model:
        returnData = {'code': 200, 'msg': '操作成功', 'data': str(model['id'])}
    else:
        returnData = {'code': 800, 'msg': '操作失败', 'data': None}
    return returnData

# ============================
# 用户注册
# ============================
@csrf_exempt
def register(request):
    post = request.POST
    if not post:
        returnData = {'code': 811, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    # 微信
    unionid = post.get('unionid')
    openid = post.get('openid')
    # 账号
    username = post.get('username')
    password = post.get('password')
    if unionid and openid:
        # 微信参数
        param = {
            'unionid': unionid,
            'openid': openid,
            'nickname': post.get('nickname'),
            'head_image_url': post.get('head_image_url'),
        }
    elif username and password:
        # 账号参数
        param = {
            'username': username,
            'password': make_password(password, None, 'pbkdf2_sha256'),
        }
    else:
        returnData = {'code': 810, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    result = _addUser(param)
    if result.get('code') == 200:
        token = QXToken(result.get('data')).generate_auth_token()
        returnData = {'code': 200, 'msg': '成功', 'data': token}
    else:
        returnData = result

    return HttpResponse(json.dumps(returnData), content_type="application/json")
