# -*- coding: utf-8 -*-

from api.controller.common_import import *  # 公共引入文件

from admin.model.User import User
from admin.model.BeanRule import BeanRule
from admin.model.Project import Project
from admin.model.BeanLog import BeanLog
from admin.model.Company import Company
from admin.model.Application import Application
from admin.model.GlobalBeanType import GlobalBeanType
# 时间模块
import datetime
import math
'''
    积分接口
'''


# ============================
# 用户积分操作api
# ============================
@csrf_exempt
def index(request):
    post = request.POST
    if not post:
        returnData = {'contract_code': 403, 'msg': '不可访问', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    request_phone = post.get('phone')
    request_action = post.get('rule_name_en')
    request_appId = post.get('app_id')  # 应用平台
    request_beans = post.get('mdBeans')  # 迈豆数
    request_token = post.get('token')
    # 获取appid配置文件
    cfg_param = configParam(request)
    api_appId_list = cfg_param.get('c_api_appId')
    try:
        request_appId = int(request_appId)
        str_appId = api_appId_list[request_appId]
    except:
        returnData = {'contract_code': -1, 'msg': '找不到配置的appId', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")

    check_token = QXToken(str_appId).verify_auth_token(request_token)  # 解析token
    if check_token and request_action and str_appId:
        # BeanRule
        try:
            # 根据条件查找规则--BeanRule
            ruleData = BeanRule.objects.get(appId=str_appId, apiName=request_action)
            need_beans = math.ceil(ruleData['ratio'] * float(request_beans))  # 需要分配给用户的迈豆数
        except:
            returnData = {'contract_code': -1, 'msg': 'rule操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if not ruleData:
            returnData = {'contract_code': -1, 'msg': '找不到对应规则', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        # Project
        try:
            # 查询Contract表，看是否有可用迈豆
            contractData = Project.objects.get(id=ruleData['project_id'])
        except:
            returnData = {'contract_code': -1, 'msg': 'contract操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if not contractData:
            returnData = {'contract_code': -1, 'msg': '找不到对应项目', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        # 根据项目起止时间判断迈豆是否可用
        now_time = datetime.datetime.now().timestamp()
        try:
            start_time = datetime.datetime.strptime(contractData['start_time'], '%Y-%m-%d').timestamp()  # 开始时间默认为0点
            end_time = datetime.datetime.strptime(contractData['end_time'], '%Y-%m-%d').timestamp() + 86400  # 截止时间默认为次日0点
            has_beans = contractData['total_beans'] - contractData['used_beans']  # 可用的迈豆数
        except:
            returnData = {'contract_code': -1, 'msg': '合同时间错误或无可用迈豆', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if now_time < start_time or now_time > end_time:
            returnData = {'contract_code': -1, 'msg': '合同不在有效期内', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if has_beans < need_beans:
            returnData = {'contract_code': -1, 'msg': '项目迈豆数不够', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        # User
        try:
            userData = User.objects.get(phone=request_phone)
        except:
            returnData = {'contract_code': -1, 'msg': 'user操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if not userData:
            returnData = {'contract_code': -1, 'msg': '找不到对应用户', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if hasattr(userData, 'beans_list'):
            userBeansList = userData['beans_list']
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
            'projectName': contractData['name_ch'],
        }
        save_beansList = dict(userBeansList, **temp_beansList)  # 合并子文档项目记录
        if hasattr(userData, 'beans_total'):
            save_beans_total = userData['beans_total'] + need_beans
        else:
            save_beans_total = + need_beans
        user_param ={
            'beans_list': save_beansList,
            'beans_total': save_beans_total,
        }
        contract_param = {
            'used_beans':contractData['used_beans'] + need_beans
        }
        try:
            user_model = User.objects.filter(phone=request_phone).update(**user_param)
        except Exception:
            returnData = {'contract_code': -1, 'msg': 'user操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        try:
            contract_model = Project.objects.get(id=contractDataId).update(**contract_param)
        except:
            returnData = {'contract_code': -1, 'msg': 'project操作失败', 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if contract_model and user_model:
            # 记录log
            log_param = {
                'company_id': contractData['company_id'],
                'app_id': contractData['app_id'],
                'project_id': str(contractData['id']),
                'project_name': contractData['name_ch'],
                'rule_id': str(ruleData['id']),
                'rule_name': ruleData['name_ch'],
                'rule_type_id': ruleData['bean_type'],
                'phone': request_phone,
                'userId': str(userData['id']),
                'rule_name_en': request_action,
                'post_beans': request_beans,
                'save_beans': need_beans,
            }
            # 查询companyName
            try:
                companyData = Company.objects.get(id=contractData['company_id'])
            except:
                companyData = None
            if companyData:
                companyDataName = companyData['name_ch']
            else:
                companyDataName = ''
            # 查询appName
            try:
                appData = Application.objects.get(id=contractData['app_id'])
            except:
                appData = None
            if appData:
                appDataName = appData['name_ch']
            else:
                appDataName = ''
            # 查询规则类型
            try:
                ruleTypeData = GlobalBeanType.objects.get(id=ruleData['bean_type'])
            except:
                ruleTypeData = None
            if ruleTypeData:
                ruleTypeDataName = ruleTypeData['name_ch']
            else:
                ruleTypeDataName = ''
            log_param.update(companyName=companyDataName)
            log_param.update(appName=appDataName)
            log_param.update(ruleTypeName=ruleTypeDataName)
            log_res = _add_log(log_param)
            if log_res['contract_code'] == 200:
                returnData = {'contract_code': 200, 'msg': '操作成功', 'data': {'user_beans': save_beans_total}}
            else:
                returnData = {'contract_code': 200, 'msg': '操作成功,log记录失败', 'data': {'user_beans': save_beans_total}}
        else:
            returnData = {'contract_code': -1, 'msg': '操作失败', 'data': None}
    else:
        returnData = {'contract_code': -2, 'msg': '参数错误', 'data': None}

    return HttpResponse(json.dumps(returnData), content_type="application/json")


# ============================
# 用户积分log记录添加--private
# ============================
def _add_log(param):
    try:
        BeanLog.objects.create(**param)
        returnData = {'contract_code': 200, 'msg': '操作成功', 'data': None}
    except Exception:
        returnData = {'contract_code': -1, 'msg': 'log记录失败', 'data': None}
    return returnData


# ============================
# 用户积分log记录查询api
# ============================
@csrf_exempt
def query(request):
    post = request.POST
    if not post:
        returnData = {'contract_code': 403, 'msg': '不可访问', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    request_phone = post.get('phone')
    if not request_phone:
        returnData = {'contract_code': -3, 'msg': '参数错误', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    request_startTime = post.get('start_time')
    request_endTime = post.get('end_time')
    param = {
        'phone': request_phone
    }
    if request_startTime:
        start_time = datetime.datetime.strptime(request_startTime, '%Y-%m-%d')  # 开始时间默认为0点
        param.update(createTime__gte=start_time)
    if request_endTime:
        end_time = datetime.datetime.strptime(request_endTime, '%Y-%m-%d') + datetime.timedelta(days=1)  # 截止时间默认为次日0点
        param.update(createTime__lte=end_time)
    try:
        beansLogData = BeanLog.objects.filter(**param).order_by('id')
    except:
        returnData = {'contract_code': 200, 'msg': 'no data', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    if beansLogData:
        data = []
        for val in beansLogData:
            createTime = val['create_time'].strftime('%Y-%m-%d %H:%M:%S')
            temp_data = {
                'company_name': val['company_name'],
                'app_name': val['app_name'],
                'rule_name': val['rule_name'],
                'saveBeans': val['save_beans'],
                'create_time': createTime,
            }
            data.append(temp_data)
        returnData = {'contract_code': 200, 'msg': 'success', 'data': data}
    else:
        returnData = {'contract_code': 200, 'msg': 'no data', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")
