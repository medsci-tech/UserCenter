# -*- coding: utf-8 -*-
'''
    用户修改基本信息接口

'''
from api.controller.common_import import *  # 公共引入文件

from admin.model.User import User as Model
from django.contrib.auth.hashers import make_password

# ============================
# 插入数据私有方法
# ============================
def _editUser(param):
    uc_uid = param.get('uc_uid')
    try:
        model = Model.objects.get(id=uc_uid).update(**param)
    except Exception:
        return ApiResponse(-3, '数据验证错误').json_return()
    if model:
        return ApiResponse(200, '操作成功', str(model['id'])).json_return()
    else:
        return ApiResponse(-1, '操作失败', str(model['id'])).json_return()

# ============================
# 修改
# ============================
@csrf_exempt
def edit(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '非法请求').json_response()
    uc_uid = post.get('uc_uid')
    token = post.get('token')
    check_token = QXToken(uc_uid).verify_auth_token(token)
    if check_token == None:
        return ApiResponse(-2, '非法操作').json_response()
    param = {
        'username': post.get('username'),
        'password': make_password(post.get('username').strip(), None, 'pbkdf2_sha256'),
    }
    result = _editUser(param)
    if result.get('contract_code') == 200:
        return ApiResponse(200, '成功').json_response()
    else:
        return ApiResponse(result).json_response()
