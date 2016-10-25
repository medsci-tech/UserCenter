# -*- coding: utf-8 -*-
'''
    公共访问方法

'''
from api.controller.common_import import *  # 公共引入文件
from admin.model.App import App
from UserCenter.global_templates import configParam

def checkAccess():
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
    '''验证token是否失效'''
    code = -1
    # token = QXToken(appId).generate_auth_token()
    # res = QXToken(appId).verify_auth_token(token)
    # if res != 200 :
    #     returnData = {'code': -1, 'msg': 'tocken失效', 'data': token}
    #     return HttpResponse(json.dumps(returnData))
    # else:
    #     return True
    returnData = {'code': 200, 'msg': '', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")


