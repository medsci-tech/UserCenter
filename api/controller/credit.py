# -*- coding: utf-8 -*-
'''
    积分接口

'''
from api.controller.common_import import *  # 公共引入文件

from admin.model.User import User
from admin.model.CreditRule import CreditRule

# ============================
# 用户积分
# ============================
@csrf_exempt
def user(request):
    post = request.POST
    if not post:
        returnData = {'code': 900, 'msg': '非法请求', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    uc_uid = post.get('uc_uid')
    action = post.get('action')
    appId = post.get('app_id')
    token = post.get('token')
    check_token = QXToken(uc_uid).verify_auth_token(token)
    if check_token and action and appId:
        '''
            查询credit_config表，看是否有可用迈豆
            查询credit_rule表，看action的相关积分规则
            根据积分规则扣掉迈豆池对应应用的积分加在用户积分上
            环节出错，回滚
        '''
        returnData = {'code': 200, 'msg': '操作成功', 'data': None}
    else:
        returnData = {'code': 901, 'msg': '非法操作', 'data': None}

    return HttpResponse(json.dumps(returnData), content_type="application/json")
