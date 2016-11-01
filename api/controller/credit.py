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
        return ApiResponse(403, '不可访问').json_response()
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
        return ApiResponse(-1, '找不到配置的appId').json_response()

    check_token = QXToken(str_appId).verify_auth_token(request_token)  # 解析token
    if check_token and request_action and str_appId:
        # BeanRule
        try:
            # 根据条件查找规则--BeanRule
            ruleData = BeanRule.objects.get(appId=str_appId, apiName=request_action)
            need_beans = math.ceil(ruleData['ratio'] * float(request_beans))  # 需要分配给用户的迈豆数
        except:
            return ApiResponse(-1, 'rule操作失败').json_response()
        if not ruleData:
            return ApiResponse(-1, '找不到对应规则').json_response()

        # Project
        try:
            # 查询Contract表，看是否有可用迈豆
            contractData = Project.objects.get(id=ruleData['project_id'])
        except:
            return ApiResponse(-1, 'contract操作失败').json_response()
        if not contractData:
            return ApiResponse(-1, '找不到对应项目').json_response()

        # 根据项目起止时间判断迈豆是否可用
        now_time = datetime.datetime.now().timestamp()
        try:
            start_time = datetime.datetime.strptime(contractData['start_time'], '%Y-%m-%d').timestamp()  # 开始时间默认为0点
            end_time = datetime.datetime.strptime(contractData['end_time'], '%Y-%m-%d').timestamp() + 86400  # 截止时间默认为次日0点
            has_beans = contractData['total_beans'] - contractData['used_beans']  # 可用的迈豆数
        except:
            return ApiResponse(-1, '合同时间错误或无可用迈豆').json_response()
        if now_time < start_time or now_time > end_time:
            return ApiResponse(-1, '合同不在有效期内').json_response()
        if has_beans < need_beans:
            return ApiResponse(-1, '项目迈豆数不够').json_response()

        # User
        try:
            userData = User.objects.get(phone=request_phone)
        except:
            return ApiResponse(-1, 'user操作失败').json_response()
        if not userData:
            return ApiResponse(-1, '找不到对应用户').json_response()
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
            return ApiResponse(-1, 'user操作失败').json_response()
        try:
            contract_model = Project.objects.get(id=contractDataId).update(**contract_param)
        except:
            return ApiResponse(-1, 'project操作失败').json_response()
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
            if log_res['code'] == 200:
                return ApiResponse(200, '操作成功', {'user_beans': save_beans_total}).json_response()
            else:
                return ApiResponse(200, '操作成功,log记录失败', {'user_beans': save_beans_total}).json_response()
        else:
            return ApiResponse(-1, '操作失败').json_response()
    else:
        return ApiResponse(-2, '参数错误').json_response()


# ============================
# 用户积分log记录添加--private
# ============================
def _add_log(param):
    try:
        BeanLog.objects.create(**param)
        return ApiResponse(200, '操作成功').json_return()
    except Exception:
        return ApiResponse(-1, 'log记录失败').json_return()


# ============================
# 用户积分log记录查询api
# ============================
@csrf_exempt
def query(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '不可访问').json_response()
    request_phone = post.get('phone')
    if not request_phone:
        return ApiResponse(-2, '参数错误').json_response()
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
        return ApiResponse(200, 'no data').json_response()
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
        return ApiResponse(200, 'success', data).json_response()
    else:
        return ApiResponse(200, 'no data').json_response()
