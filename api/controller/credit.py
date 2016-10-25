# -*- coding: utf-8 -*-
'''
    积分接口

'''
from api.controller.common_import import *  # 公共引入文件

from admin.model.User import User
from admin.model.CreditRule import CreditRule
from admin.model.Contract import Contract
# 时间模块
from datetime import *

# ============================
# 用户积分
# ============================
@csrf_exempt
def index(request):
    post = request.POST
    if not post:
        returnData = {'code': 403, 'msg': '不可访问', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    request_phone = post.get('phone')
    request_action = post.get('action')
    request_appId = int(post.get('app_id'))  # 应用平台
    request_beans = post.get('md_beans')  # 迈豆数
    request_token = post.get('token')
    # 获取appid配置文件
    cfg_param = configParam(request)
    api_appId_list = cfg_param.get('c_api_appId')
    check_token = QXToken(request_phone).verify_auth_token(request_token)  # 解析token
    if check_token and request_action and request_appId:
        '''
            查询contract表，看是否有可用迈豆
            查询credit_rule表，看action的相关积分规则
            根据积分规则扣掉迈豆池对应应用的积分加在用户积分上
            环节出错，回滚
        '''
        str_appId = api_appId_list[request_appId]
        try:
            # 根据条件查找规则
            ruleData = CreditRule.objects.get(appId=str_appId, apiName=request_action)
        except:
            returnData = {'code': -1, 'msg': '操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if not ruleData:
            returnData = {'code': -1, 'msg': '找不到对应规则', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        try:
            # 查询contract表，看是否有可用迈豆
            contractData = Contract.objects.get(id=ruleData['contractId'])
        except:
            returnData = {'code': -1, 'msg': '操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if not contractData:
            returnData = {'code': -1, 'msg': '找不到对应项目', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        # 根据项目起止时间判断迈豆是否可用
        now_time = datetime.now().timestamp()
        try:
            start_time = datetime.strptime(contractData['startTime'], "%Y-%m-%d").timestamp()  # 开始时间默认为0点
            end_time = datetime.strptime(contractData['endTime'], "%Y-%m-%d").timestamp() + 86400  # 截止时间默认为次日0点
        except:
            returnData = {'code': -1, 'msg': '合同时间错误', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if now_time < start_time or now_time > end_time:
            returnData = {'code': -1, 'msg': '合同不在有效期内', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if now_time < start_time or now_time > end_time:
            returnData = {'code': -1, 'msg': '合同不在有效期内', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        returnData = {'code': 200, 'msg': '操作成功', 'data': start_time}
    else:
        returnData = {'code': -2, 'msg': '参数缺失', 'data': None}

    return HttpResponse(json.dumps(returnData), content_type="application/json")
