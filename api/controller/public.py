# -*- coding: utf-8 -*-
'''
    公共访问方法

'''
from api.controller.common_import import *  # 公共引入文件
from admin.model.User import User as Model
from admin.model.Application import Application
from django.contrib.auth.hashers import check_password, make_password
# configParam
from UserCenter.global_templates import configParam
from api.controller.common import checkAccess
from api.controller.funForMime import imitate_post
from django.http import HttpRequest
import re
import base64
import hashlib
import time
# ============================
# 获取token
# ============================
@csrf_exempt
def get_token(request):
    post = request.POST
    if not post:
        returnData = {'contract_code': 403, 'msg': '无效请求!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")

    appId = int(post.get('app_id',0))
    cfg_param = configParam(request)
    try:
        appId = cfg_param.get('c_api_appId')[appId]
        res = Application.objects.get(id=appId)
        if not res :
            returnData = {'contract_code': -1, 'msg': '该应用id不存在', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
    except (ValueError, KeyError, TypeError):
        return HttpResponse(json.dumps({'contract_code': -1, 'msg': '该应用id不存在!', 'data': None}), content_type="application/json")

    token = QXToken(appId).generate_auth_token()
    res = QXToken(appId).verify_auth_token(token)
    returnData = {'contract_code': 200, 'msg': '成功', 'data': token}
    return HttpResponse(json.dumps(returnData), content_type="application/json")

# ============================
# 查询单条数据私有方法
# ============================
def _getUser(param, data_param):
    try:
        model = Model.objects.get(**param)
    except Exception:
        return {'contract_code': 200, 'msg': '可以注册!!', 'data': None}
    if model:
        returnData = {'contract_code': -1, 'msg': '用户已经存在!', 'data': None}
    else:
        returnData = {'contract_code': 200, 'msg': '可以注册!', 'data': None}
    return returnData

# ============================
# 用户登录
# ============================
@csrf_exempt
def login(request):
    post = request.POST
    if not post:
        returnData = {'contract_code': 811, 'msg': '非法请求', 'data': None}
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
        returnData = {'contract_code': 811, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    result = _getUser(param, data_param)
    if result.get('contract_code') == 200:
        if data_param == 'password':
            check_code = check_password(password, result.get('data')[data_param])
        else:
            check_code = (result.get('data')[data_param] == check_value)
        if check_code:
            uc_uid = result.get('data')['uc_uid']
            token = QXToken(uc_uid).generate_auth_token()
            returnData = {'contract_code': 200, 'msg': '成功', 'data': {'uc_uid': uc_uid, 'token': token}}
        else:
            returnData = {'contract_code': 910, 'msg': '失败', 'data': None}
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
    if check_exist.get('contract_code') == -1:
        return {'contract_code': 200, 'msg': '用户已存在', 'data': None}
    try:
        model = Model.objects.create(**param)
    except Exception:
        return {'contract_code': -1, 'msg': '数据验证错误!', 'data': param}
    if model:
        returnData = {'contract_code': 200, 'msg': '注册成功!', 'data':None}
    else:
        returnData = {'contract_code': 800, 'msg': '注册失败', 'data': None}
    return returnData
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

# ============================
# 检查密码合法性
# ============================
def checkPassword(pwd):
    pass

# ============================
# 用户注册
# ============================
@csrf_exempt
def register(request):
    post = request.POST
    if not post:
        returnData = {'contract_code': 403, 'msg': '无效请求!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    longitude = post.get('longitude', None)  # 经度
    latitude = post.get('latitude', None)  # 纬度
    phone = post.get('phone')  # 用户名
    password = post.get('password')  # 密码

    # post_url = 'http://' + HttpRequest.get_host(request) + '/api/credit/index'
    # post_param = {
    #     'phone': phone,
    #     'rule_name_en': 'register',
    #     'app_id': post.get('app_id'),
    #     'mdBeans': post.get('mdBeans'),
    #     'token': post.get('token'),
    # }
    # returnData = imitate_post(url=post_url, param=post_param)
    # return HttpResponse(json.dumps(post_url), content_type="application/json")

    if not(phone and password):
        returnData = {'contract_code': -1, 'msg': '用户或密码不能为空', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        '''验证密码合法性'''
        if len(password) < 80:
            returnData = {'contract_code': -3, 'msg': '密码不能明文传输!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        try:
            password = tcodes(password, isEncrypt=0, key='mime.org.cn')  # 解密
        except:
            returnData = {'contract_code': -3, 'msg': '参数解析失败!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if phone:
            phone.strip()
        if password:
            password.strip()

        patten = re.findall(r'\d+', password)
        if password.isalpha() or password.isnumeric() or not patten:
            returnData = {'contract_code': -3, 'msg': '密码必须包含字母和数字!允许有特殊符号!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if len(password) > 30 or len(password) < 6:
            returnData = {'contract_code': -3, 'msg': '密码长度介于6-30个字符!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

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
            returnData = {'contract_code': -1, 'msg': '用户已经存在!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        else :
            result = Model.objects.create(**param) # 注册用户
    except (ValueError, KeyError, TypeError):
        return {'contract_code': -1, 'msg': '服务器异常!', 'data': None}

    if result:
        # 积分
        post_url = 'http://' + HttpRequest.get_host(request) + '/api/credit/index'
        post_param = {
            'phone': phone,
            'rule_name_en': 'register',
            'app_id': post.get('app_id'),
            'mdBeans': post.get('mdBeans',1),
            'token': post.get('token'),
        }
        returnData = imitate_post(url=post_url, param=post_param)
    else:
        returnData = {'contract_code': -1, 'msg': '注册失败!', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")

@csrf_exempt
def setPwd(request):
    post = request.POST
    if not post:
        returnData = {'contract_code': 403, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    phone = post.get('phone')
    password = post.get('password')
    repassword = post.get('repassword')
    if phone == '':
        returnData = {'contract_code': -2, 'msg': '用户名不能为空!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")

    if password == '':
        returnData = {'contract_code': -2, 'msg': '密码不能为空!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")

    '''验证密码合法性'''
    if len(password)<80:
        returnData = {'contract_code': -3, 'msg': '密码不能明文传输!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    try:
        password = tcodes(password, isEncrypt=0, key='mime.org.cn') #解密
        repassword = tcodes(repassword, isEncrypt=0, key='mime.org.cn')  # 解密
    except:
        returnData = {'contract_code': -3, 'msg': '参数解析失败!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    if phone:
        phone.strip()
    if password:
        password.strip()
    if repassword:
        repassword.strip()

    patten = re.findall(r'\d+', password)
    if password.isalpha() or password.isnumeric() or not patten:
        returnData = {'contract_code': -3, 'msg': '密码必须包含字母和数字!允许有特殊符号!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    if len(password)>30 or len(password)<6:
        returnData = {'contract_code': -3, 'msg': '密码长度介于6-30个字符!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    if password != repassword:
        returnData = {'contract_code': -3, 'msg': '两次输入的密码不一致!', 'data': None}
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
            returnData = {'contract_code': 200, 'msg': '密码设置成功!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        else:
            returnData = {'contract_code': -4, 'msg': '该用户不存在!', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
    except (ValueError, KeyError, TypeError):
        returnData = {'contract_code': 500, 'msg': '服务器操作异常!', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")








