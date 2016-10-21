# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.CreditRule import CreditRule as Model
from admin.controller.app import applist
from admin.controller.company import companylist

'''
迈豆积分列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    get = request.GET
    param = {}
    # 获取所有启用应用列表
    company_list = companylist(request)

    # 获取配置列表
    searchCompanyId = get.get('companyId')
    if searchCompanyId:
        param.update(companyId=searchCompanyId)
    else:
        dataOne = Model.objects.filter().order_by('id')[:1]  # 获取第一条数据
        if dataOne:
            param.update(companyId=dataOne[0]['companyId'])
    data = Model.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表

    if data:
        selectData = data[0]
    else:
        selectData = get

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)
    app_list = applist(request, companyId=selectData['companyId'])
    # return HttpResponse(credit_list)
    return render(request, 'admin/credit_rule/index.html', {
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': selectData,
        'companyList': company_list,
        'appList': app_list,
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
        name = post.get('name')
        appId = post.get('appId')
        try:
            check_name = Model.objects.filter(name=name, appId=appId).order_by('id')
        except Exception:
            returnData = {'code': 808, 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if check_name:
            returnData = {'code': 808, 'msg': '策略字段%s已存在' % name, 'data': None}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        extend_list = {}
        # 获取配置列表
        cfg_param = configParam(request)
        ext_credit_list = cfg_param.get('c_ext_credit')
        for key in ext_credit_list:
            extend_list[str(key)] = post.get('extend[' + key + ']', 0)
        param = {
            'appId': appId,
            'companyId': post.get('companyId'),
            'name': name,
            'remark': post.get('remark'),
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
