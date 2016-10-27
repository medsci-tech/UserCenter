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
from api.controller.funForMime import imitate_post
from django.http import HttpRequest
# ============================
# 获取token
# ============================
@csrf_exempt
def get_token(request):
    post = request.POST
    if not post:
        returnData = {'code': 403, 'msg': '无效请求!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")

    appId = int(post.get('appId',0))
    cfg_param = configParam(request)
    try:
        appId = cfg_param.get('c_api_appId')[appId]
        res = App.objects.get(id=appId)
        if not res :
            returnData = {'code': -1, 'msg': '该应用id不存在', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
    except (ValueError, KeyError, TypeError):
        return HttpResponse(json.dumps({'code': -1, 'msg': '该应用id不存在!', 'data': None}), content_type="application/json")

    token = QXToken(appId).generate_auth_token()
    res = QXToken(appId).verify_auth_token(token)
    returnData = {'code': 200, 'msg': '成功', 'data': token}
    return HttpResponse(json.dumps(returnData), content_type="application/json")

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
    phone = post.get('phone')
    password = post.get('password')
    if unionid and openid:
        # 微信参数
        param = {
            'unionid': unionid,
        }
        data_param = 'openid'
        check_value = openid
    elif phone and password:
        # 账号参数
        param = {
            'phone': phone,
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
    phone = param.get('phone')
    check_param = {
        'phone': phone,
    }
    data_param = 'phone'
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
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    longitude = post.get('longitude', None)  # 经度
    latitude = post.get('latitude', None)  # 纬度
    phone = post.get('phone')  # 用户名
    password = post.get('password')  # 密码

    # post_url = 'http://' + HttpRequest.get_host(request) + '/api/credit/index'
    # post_param = {
    #     'phone': phone,
    #     'action': 'register',
    #     'appId': post.get('appId'),
    #     'mdBeans': post.get('mdBeans'),
    #     'token': post.get('token'),
    # }
    # returnData = imitate_post(url=post_url, param=post_param)
    # return HttpResponse(json.dumps(post_url), content_type="application/json")

    if not(phone and password):
        returnData = {'code': -1, 'msg': '用户或密码不能为空', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        # 注册参数
        param = {
            'phone': phone,
            'password': make_password(password, None, 'pbkdf2_sha256'),
            'longitude': longitude,
            'latitude': latitude,
        }
    try:
        model = Model.objects.filter(phone=phone)
        if model:
            returnData = {'code': -1, 'msg': '用户已经存在!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        else :
            result = Model.objects.create(**param) # 注册用户
    except (ValueError, KeyError, TypeError):
        return {'code': -1, 'msg': '服务器异常!', 'data': None}

    if result:
        # 积分
        post_url = 'http://' + HttpRequest.get_host(request) + '/api/credit/index'
        post_param = {
            'phone': phone,
            'action': 'register',
            'appId': post.get('appId'),
            'mdBeans': post.get('mdBeans'),
            'token': post.get('token'),
        }
        returnData = imitate_post(url=post_url, param=post_param)
    else:
        returnData = {'code': -1, 'msg': '注册失败!', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")

# ============================
# 设置/修改密码
# ============================
@csrf_exempt
def setPwd(request):
    post = request.POST
    if not post:
        returnData = {'code': 403, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    phone = post.get('phone')
    if phone:
        phone.strip()
    password = post.get('password')
    if password:
        password.strip()
    repassword = post.get('repassword')
    if repassword:
        repassword.strip()

    if phone == '':
        returnData = {'code': -2, 'msg': '用户名不能为空!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    if password == '':
        returnData = {'code': -2, 'msg': '密码不能为空!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    if len(password)>12 :
        returnData = {'code': -3, 'msg': '密码长度不能超过12个字符!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    if password != repassword:
        returnData = {'code': -1, 'msg': '两次输入的密码不一致!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")

    '''验证用户名是否存在'''
    try:
        model = Model.objects.filter(phone=phone)
        if model:
            password = make_password(password, None, 'pbkdf2_sha256')
            param = {
                'password': password
            }
            Model.objects.filter(phone=phone).update(**param)
            returnData = {'code': 200, 'msg': '密码设置成功!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        else:
            returnData = {'code': -4, 'msg': '该用户不存在!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
    except (ValueError, KeyError, TypeError):
        return {'code': 500, 'msg': '服务器操作异常!', 'data': None}





