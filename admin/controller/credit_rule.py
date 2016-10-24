# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.CreditRule import CreditRule as Model
from admin.model.IntegralType import IntegralType
from admin.model.Contract import Contract
from admin.model.App import App
from admin.model.Company import Company

'''
迈豆积分列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    get = request.GET
    post = request.POST
    param = {}
    searchContractId = get.get('contractId')
    searchName = post.get('name')
    if searchContractId:
        param.update(contractId=searchContractId)
        if searchName:
            param.update(name={'$regex': searchName})
        data = Model.objects.filter(**param).order_by("id")
        contractData = Contract.objects.filter(status=1, id=searchContractId).order_by("id")[:1][0]
        appData = App.objects.filter(status=1, id=contractData['appId']).order_by("id")[:1][0]
        companyData = Company.objects.filter(status=1, id=contractData['companyId']).order_by("id")[:1][0]
    else:
        data = {}
        contractData = {}
        appData = {}
        companyData = {}

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)
    integralType = IntegralType.objects.filter(status=1).order_by('id')
    # return HttpResponse(credit_list)
    return render(request, 'admin/credit_rule/index.html', {
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
        'form_contractData': contractData,
        'list_integralType': integralType,
        'form_appData': appData,
        'form_companyData': companyData,
    })

# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = Model.objects.create(**param)
            if model:
                returnData = {'code': '200', 'msg': '操作成功', 'data': str(model['id'])}
            else:
                returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}
    else:
        returnData = {'code': '901', 'msg': '数据错误', 'data': ''}
    return returnData

# 修改操作--protected
def _editById(**param):
    id = param.get('id')
    if id:
        try:
            model = Model.objects.get(id=id).update(**param)
        except Exception:
            return {'code': '900', 'msg': '数据验证错误', 'data': Exception}
        if model:
            returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
    else:
        returnData = {'code': '901', 'msg': '数据错误', 'data': ''}
    return returnData

# 修改操作
@auth  # 引用登录权限验证
def form(request):
    post = request.POST
    if post:
        id = post.get('id')
        apiName = post.get('apiName')
        contractId = post.get('contractId')
        try:
            check_name = Model.objects.filter(apiName=apiName).order_by('id')[:1]
        except Exception:
            returnData = {'code': 802, 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if check_name:
            if str(check_name[0]['id']) != id:
                returnData = {'code': 801, 'msg': '策略字段%s已存在' % apiName, 'data': None}
                return HttpResponse(json.dumps(returnData), content_type="application/json")
        extend_list = {}
        # 获取配置列表
        cfg_param = configParam(request)
        ext_credit_list = cfg_param.get('c_ext_credit')
        for key in ext_credit_list:
            extend_list[str(key)] = post.get('extend[' + key + ']', 0)
        param = {
            'appId': post.get('appId'),
            'companyId': post.get('companyId'),
            'contractId': contractId,
            'apiName': apiName,
            'integralType': post.get('integralType'),
            'name': post.get('name'),
            'cycle': post.get('cycle'),
            'rewardNum': post.get('rewardNum'),
            'extend': extend_list,
            'status': post.get('status'),
        }
        if id:
            # 修改
            param.update(id=id)
            returnData = _editById(**param)
        else:
            # 添加
            returnData = _add(**param)

        # 操作成功添加log操作记录
        if returnData.get('code') == '200':
            # log记录参数
            logParam = {
                'table': 'credit_rule',
                'after': param,
            }
            if id:
                logParam.update(tableId=id)  # log记录参数
                logParam.update(action=2)  # log记录参数,action=2为修改
            else:
                logParam.update(tableId=returnData.get('data'))  # log记录参数
                logParam.update(action=1)  # log记录参数,action=1为添加
            if 'id' in logParam['after']:
                del logParam['after']['id']
            logsform(request, logParam)
    else:
        returnData = {'code': '1000', 'msg': '不允许直接访问', 'data': None}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

# 更改状态操作
@auth  # 引用登录权限验证
def stats(request):
    post = request.POST
    if post:
        selection = post.getlist('selection[]')
        statusType = post.get('statusType')
        if statusType == 'enable':
            status = 1
        else:
            status = 0
        param = {
            'status': status,
        }
        try:
            model = Model.objects.filter(id__in=selection).update(**param)
            if model:
                # 操作成功添加log操作记录
                for id in selection:
                    # log记录参数
                    logParam = {
                        'table': 'credit_rule',
                        'after': param,
                        'tableId': id,
                    }
                    if statusType == 'enable':
                        logParam.update(action=3)  # log记录参数,action=3为启用
                    else:
                        logParam.update(action=4)  # log记录参数,action=4为禁用
                    if 'id' in logParam['after']:
                        del logParam['after']['id']
                    logsform(request, logParam)

                returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
            else:
                returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
        except Exception:
                returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}

        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        returnData = {'code': '1000', 'msg': '不允许直接访问', 'data': None}
        return HttpResponse(json.dumps(returnData), content_type="application/json")
