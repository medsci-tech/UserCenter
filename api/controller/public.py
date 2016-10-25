# -*- coding: utf-8 -*-
'''
    公共访问方法

'''
from api.controller.common_import import *  # 公共引入文件
from admin.model.User import User as Model
from admin.model.App import App
from django.contrib.auth.hashers import check_password, make_password
# configParam
from UserCenter.global_templates import configParam
from api.controller.common import checkAccess
# ============================
# 获取token
# ============================
@csrf_exempt
def get_token(request):
    post = request.POST
    if not post:
        returnData = {'code': 403, 'msg': '无效请求!', 'data': None}
        return HttpResponse(json.dumps(returnData))

    appId = int(post.get('appId',0))
    cfg_param = configParam(request)
    try:
        appId = cfg_param.get('c_api_appId')[appId]
        res = App.objects.get(id=appId)
        if not res :
            returnData = {'code': -1, 'msg': '该应用id不存在', 'data': None}
            return HttpResponse(json.dumps(returnData))
    except (ValueError, KeyError, TypeError):
        return HttpResponse(json.dumps({'code': -1, 'msg': '该应用id不存在!', 'data': None}))

    token = QXToken(appId).generate_auth_token()
    res = QXToken(appId).verify_auth_token(token)
    returnData = {'code': 200, 'msg': '成功', 'data': token}
    return HttpResponse(json.dumps(returnData))

# ============================
# 查询单条数据私有方法
# ============================
def _getUser(param, data_param):
    try:
        model = Model.objects.get(**param)
    except Exception:
        return {'code': 200, 'msg': '可以注册!!', 'data': None}
    if model:
        returnData = {'code': -1, 'msg': '用户已经存在!', 'data': None}
    else:
        returnData = {'code': 200, 'msg': '可以注册!', 'data': None}
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
    if result.get('code') == 200:
        if data_param == 'password':
            check_code = check_password(password, result.get('data')[data_param])
        else:
            check_code = (result.get('data')[data_param] == check_value)
        if check_code:
            uc_uid = result.get('data')['uc_uid']
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
    check_param = {
        'username': username,
    }
    data_param = 'username'
    return {'code': 200, 'msg': '用户已存在', 'data': None}

    check_exist = _getUser(check_param, data_param)
    if check_exist.get('code') == -1:
        return {'code': 200, 'msg': '用户已存在', 'data': None}
    try:
        model = Model.objects.create(**param)
    except Exception:
        return {'code': -1, 'msg': '数据验证错误!', 'data': param}
    if model:
        returnData = {'code': 200, 'msg': '注册成功!', 'data':None}
    else:
        returnData = {'code': 800, 'msg': '注册失败', 'data': None}
    return returnData

# ============================
# 用户注册
# ============================
@csrf_exempt
def register(request):

    post = request.POST
    if not post:
        returnData = {'code': 403, 'msg': '无效请求!', 'data': None}
        return HttpResponse(json.dumps(returnData))
    longitude = post.get('longitude',None) # 经度
    latitude = post.get('latitude',None) # 纬度
    username = post.get('username') # 用户名
    password = post.get('password') # 密码

    if not(username and password):
        returnData = {'code': -1, 'msg': '用户或密码不能为空', 'data': None}
        return HttpResponse(json.dumps(returnData))
    else:
        # 注册参数
        param = {
            'username': username,
            'password': make_password(password, None, 'pbkdf2_sha256'),
            'longitude': longitude,
            'latitude': latitude,
        }
    try:
        model = Model.objects.filter(username=username)
        if model:
            returnData = {'code': -1, 'msg': '用户已经存在!', 'data': None}
            return HttpResponse(json.dumps(returnData))
        else :
            result = Model.objects.create(**param) # 注册用户
            if result :
                pass
            '''获取积分接口'''
    except (ValueError, KeyError, TypeError):
        return {'code': -1, 'msg': '服务器异常!', 'data': None}

    if result:
        returnData = {'code': 200, 'msg': '注册成功!', 'data': None}
    else:
        returnData = {'code': -1, 'msg': '注册失败!', 'data': None}
    return HttpResponse(json.dumps(returnData))
