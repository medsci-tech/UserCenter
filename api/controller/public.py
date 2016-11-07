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
        return ApiResponse(403, '无效请求').json_response()

    appId = int(post.get('app_id'))
    cfg_param = configParam(request)
    try:
        appId = cfg_param.get('c_api_appId')[appId]
        res = Application.objects.get(id=appId)
    except:
        return ApiResponse(-1, '该应用id不存在').json_response()
    if res:
        token = QXToken(appId).generate_auth_token()
        return ApiResponse(200, '成功', token).json_response()
    else:
        return ApiResponse(-1, '该应用id不存在').json_response()

# ============================
# 查询单条数据私有方法
# ============================
def _getUser(param, data_param):
    try:
        model = Model.objects.get(**param)
    except Exception:
        return ApiResponse(-1, '参数错误').json_return()
    if model:
         # data =
        return ApiResponse(200, '成功',  {
             '%s' % data_param: model[data_param],
             'uc_uid': str(model['id']),
         }).json_return()
    else:
        return ApiResponse(-4, '不存在').json_return()


# ============================
# 用户登录
# ============================
@csrf_exempt
def login(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '非法请求').json_response()
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
        return ApiResponse(403, '非法请求').json_response()
    result = _getUser(param, data_param)
    json_result = json.loads(result)
    if json_result.get('code') == -4:
        return ApiResponse(-1, '用户不存在').json_response()
    if json_result.get('code') == 200:
        if data_param == 'password':
            check_code = check_password(password, json_result.get('data')[data_param])
        else:
            check_code = (json_result.get('data')[data_param] == check_value)
        if check_code:
            uc_uid = json_result.get('data')['uc_uid']
            token = QXToken(uc_uid).generate_auth_token()
            return ApiResponse(200, '成功', {'uc_uid': uc_uid, 'token': token}).json_response()
        else:
            return ApiResponse(-1, '失败').json_response()
    else:
        return HttpResponse(result, content_type="application/json")

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
    if json.loads(check_exist.get('code')) == 200:
        return ApiResponse(-1, '用户已存在').json_return()
    try:
        model = Model.objects.create(**param)
    except Exception:
        return ApiResponse(-1, '数据验证错误', param).json_return()
    if model:
        return ApiResponse(200, '注册成功').json_return()
    else:
        return ApiResponse(-1, '注册失败').json_return()


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
        return ApiResponse(403, '无效请求').json_response()
    longitude = post.get('longitude', None)  # 经度
    latitude = post.get('latitude', None)  # 纬度
    phone = post.get('phone')  # 用户名
    password = post.get('password')  # 密码

    if not(phone and password):
        return ApiResponse(-1, '用户或密码不能为空').json_response()
    else:
        '''验证密码合法性'''
        # if len(password) < 80:
        #     return ApiResponse(-3, '密码不能明文传输').json_response()
        # try:
        #     password = tcodes(password, isEncrypt=0, key='mime.org.cn')  # 解密
        # except:
        #     return ApiResponse(-3, '参数解析失败').json_response()
        if phone:
            phone.strip()
        if password:
            password.strip()

        patten = re.findall(r'\d+', password)
        if password.isalpha() or password.isnumeric() or not patten:
            return ApiResponse(-3, '密码必须包含字母和数字,允许有特殊符号').json_response()
        if len(password) > 30 or len(password) < 6:
            return ApiResponse(-3, '密码长度介于6-30个字符').json_response()

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
            return ApiResponse(-1, '用户已经存在').json_response()
        else :
            result = Model.objects.create(**param) # 注册用户
    except (ValueError, KeyError, TypeError):
        return ApiResponse(-1, '服务器异常').json_response()

    if result:
        # 积分
        post_url = 'http://' + HttpRequest.get_host(request) + '/api/credit/index'
        post_param = {
            'phone': phone,
            'rule_name_en': 'register',
            'app_id': post.get('app_id'),
            'md_beans': post.get('md_beans',1),
            'token': post.get('token'),
        }
        returnData = imitate_post(url=post_url, param=post_param)
        return ApiResponse(200, returnData['msg'], returnData['data']).json_response()
    else:
        return ApiResponse(-1, '注册失败').json_response()

@csrf_exempt
def setPwd(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '非法请求').json_response()
    phone = post.get('phone')
    password = post.get('password')
    repassword = post.get('repassword')
    if phone == '' or password == '':
        return ApiResponse(-2, '用户名或密码不能为空').json_response()

    '''验证密码合法性'''
    # if len(password)<80:
    #     return ApiResponse(-3, '密码不能明文传输').json_response()
    # try:
    #     password = tcodes(password, isEncrypt=0, key='mime.org.cn') #解密
    #     repassword = tcodes(repassword, isEncrypt=0, key='mime.org.cn')  # 解密
    # except:
    #     return ApiResponse(-3, '参数解析失败').json_response()
    if phone:
        phone.strip()
    if password:
        password.strip()
    if repassword:
        repassword.strip()

    patten = re.findall(r'\d+', password)
    if password.isalpha() or password.isnumeric() or not patten:
        return ApiResponse(-3, '密码必须包含字母和数字,允许有特殊符号').json_response()
    if len(password)>30 or len(password)<6:
        return ApiResponse(-3, '密码长度介于6-30个字符').json_response()
    if password != repassword:
        return ApiResponse(-3, '两次输入的密码不一致').json_response()

    '''验证用户名是否存在'''
    try:
        model = Model.objects.filter(phone=phone)
        if model:
            password = make_password(password, None, 'pbkdf2_sha256')
            param = {
                'password': password
            }
            Model.objects.filter(phone=phone).update(**param)
            return ApiResponse(200, '密码设置成功').json_response()
        else:
            return ApiResponse(-4, '该用户不存在').json_response()
    except (ValueError, KeyError, TypeError):
        return ApiResponse(-3, '服务器操作异常').json_response()








