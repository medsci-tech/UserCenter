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
import math
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
    request_appId = post.get('appId')  # 应用平台
    request_beans = post.get('mdBeans')  # 迈豆数
    request_token = post.get('token')
    # 获取appid配置文件
    cfg_param = configParam(request)
    api_appId_list = cfg_param.get('c_api_appId')
    request_appId = int(request_appId)
    str_appId = api_appId_list[request_appId]
    check_token = QXToken(str_appId).verify_auth_token(request_token)  # 解析token
    if check_token and request_action and str_appId:
        # CreditRule
        try:
            # 根据条件查找规则--CreditRule
            ruleData = CreditRule.objects.get(appId=str_appId, apiName=request_action)
            need_beans = math.ceil(ruleData['ratio'] * float(request_beans))  # 需要分配给用户的迈豆数
        except:
            returnData = {'code': -1, 'msg': '操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if not ruleData:
            returnData = {'code': -1, 'msg': '找不到对应规则', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        # Contract
        try:
            # 查询Contract表，看是否有可用迈豆
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
            has_beans = contractData['totalBeans'] - contractData['useBeans']  # 可用的迈豆数
        except:
            returnData = {'code': -1, 'msg': '合同时间错误或无可用迈豆', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if now_time < start_time or now_time > end_time:
            returnData = {'code': -1, 'msg': '合同不在有效期内', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if has_beans < need_beans:
            returnData = {'code': -1, 'msg': '项目迈豆数不够', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        # User
        try:
            userData = User.objects.get(phone=request_phone)
        except:
            returnData = {'code': -1, 'msg': '操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if not userData:
            returnData = {'code': -1, 'msg': '找不到对应用户', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if hasattr(userData, 'beansList'):
            userBeansList = userData['beansList']
        else:
            userBeansList = {}
        # 查询用户是否已经有该项目记录
        temp_beansList = {}
        contractDataId = str(contractData['id'])
        if contractDataId in userBeansList.keys():
            temp_beans = userBeansList[contractDataId]['beans'] + need_beans
        else:
            temp_beans = need_beans
        temp_beansList[contractDataId] = {
            'beans': temp_beans,
        }
        save_beansList = dict(userBeansList, **temp_beansList)  # 合并子文档项目记录
        save_beans_total = userData['beans_total'] + need_beans
        user_param ={
            'beansList': save_beansList,
            'beans_total': save_beans_total,
        }
        contract_param = {
            'useBeans':contractData['useBeans'] + need_beans
        }
        try:
            user_model = User.objects.filter(phone=request_phone).update(**user_param)
        except Exception:
            returnData = {'code': -1, 'msg': 'user操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        try:
            contract_model = Contract.objects.get(id=contractDataId).update(**contract_param)
        except:
            returnData = {'code': -1, 'msg': 'project操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if contract_model and user_model:
            returnData = {'code': 200, 'msg': '操作成功', 'data': {'user_beans': save_beans_total}}
        else:
            '''
                回滚数据
            '''
            returnData = {'code': -2, 'msg': '操作失败', 'data': None}
    else:
        returnData = {'code': -2, 'msg': '参数缺失', 'data': check_token}

    return HttpResponse(json.dumps(returnData), content_type="application/json")


# ============================
# 用户
# ============================