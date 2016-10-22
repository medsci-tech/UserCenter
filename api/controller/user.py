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
        return {'code': 808, 'msg': '数据验证错误', 'data': None}
    if model:
        returnData = {'code': 200, 'msg': '操作成功', 'data': str(model['id'])}
    else:
        returnData = {'code': 800, 'msg': '操作失败', 'data': None}
    return returnData

# ============================
# 修改
# ============================
@csrf_exempt
def edit(request):
    post = request.POST
    if not post:
        returnData = {'code': 900, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    uc_uid = post.get('uc_uid')
    token = post.get('token')
    check_token = QXToken(uc_uid).verify_auth_token(token)
    if check_token == None:
        return {'code': 901, 'msg': '非法操作', 'data': None}
    param = {
        'username': post.get('username'),
        'password': make_password(post.get('username').strip(), None, 'pbkdf2_sha256'),
    }
    result = _editUser(param)
    if result.get('code') == 200:
        returnData = {'code': 200, 'msg': '成功', 'data': None}
    else:
        returnData = result

    return HttpResponse(json.dumps(returnData), content_type="application/json")
