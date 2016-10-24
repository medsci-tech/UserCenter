# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.Contract import Contract as Model
from admin.model.App import App
from admin.model.Company import Company

'''
迈豆积分列表
'''
@csrf_exempt
@auth  # 引用登录权限验证
def index(request):
    get = request.GET
    post = request.POST
    param = {}
    # 获取所有状态列表
    searchAppId = get.get('appId')
    searchName = post.get('name')
    if searchAppId:
        param.update(appId=searchAppId)
        if searchName:
            param.update(name={'$regex': searchName})
        data = Model.objects.filter(**param).order_by("id")
        appData = App.objects.filter(status=1, id=searchAppId).order_by("id")[:1][0]
        companyData = Company.objects.filter(status=1, id=appData['companyId']).order_by("id")[:1][0]
    else:
        data = {}
        appData = {}
        companyData = {}

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)
    return render(request, 'admin/credit_config/index.html', {
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
        'form_appData': appData,
        'form_companyData': companyData,
    })

# 修改操作--protected
def _editById(**param):
    id = param.get('id')
    if id:
        try:
            model = Model.objects.get(id=id).update(**param)
            if model == 1:
                returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
            else:
                returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}
    else:
        returnData = {'code': '901', 'msg': '数据错误', 'data': ''}
    return returnData

# 修改操作
@auth  # 引用登录权限验证
def form(request):
    post = request.POST
    if post:
        id = post.get('id')
        contractId = post.get('contractId')
        try:
            check_name = Model.objects.filter(contractId=contractId).order_by('id')
        except Exception:
            returnData = {'code': 801, 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if check_name:
            if str(check_name[0]['id']) != id:
                returnData = {'code': 802, 'msg': '合同已有对应的迈豆池', 'data': None}
                return HttpResponse(json.dumps(returnData), content_type="application/json")
        extend_list = {}
        # 获取配置列表
        cfg_param = configParam(request)
        ext_credit_list = cfg_param.get('c_ext_credit')
        for key in ext_credit_list:
            extend_list[str(key)] = post.get('extend[' + key + ']', 0)
        param = {
            'appId': post.get('appId'),
            'apiName': post.get('remarkName'),
            'extend': extend_list,
            'status': post.get('status'),
        }
        if id:
            # 修改
            param.update(id=id)
            returnData = _editById(**param)
        else:
            returnData = {'code': 805, 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")

        # 操作成功添加log操作记录
        if returnData.get('code') == '200':
            # log记录参数
            logParam = {
                'table': 'credit_config',
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
                        'table': 'credit_config',
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

'''
前端访问接口
'''
@auth  # 引用登录权限验证
def creditconfiglist(request, **kwargs):
    if request.method == 'POST':
        req = request.POST
        appId = req.get('appId')
    else:
        appId = kwargs.get('appId')
    returnFormat = kwargs.get('returnFormat')
    if appId:
        data = {}
        try:
            app = Model.objects.filter(status=1, appId=appId).order_by("id")
        except Exception:
            app = {}
        if app:
            for val in app:
                data[str(val.id)] = val.remarkName
        if data:
            returnData = {'code': 200, 'msg': '操作成功', 'data': data}
        else:
            returnData = {'code': 200, 'msg': '暂无数据', 'data': None}
    else:
        returnData = {'code': 200, 'msg': '参数缺失', 'data': None}

    if returnFormat:
        return returnData.get('data')
    elif request.method == 'POST':
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        return returnData.get('data')
