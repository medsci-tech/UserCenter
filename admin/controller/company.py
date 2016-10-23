# -*- coding: utf-8 -*-
# 企业管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.Company import Company as Model
from admin.model.App import App
from admin.model.CreditRule import CreditRule
from admin.model.Contract import Contract

'''
迈豆积分列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    param = {}
    # 获取配置列表
    cfg_param = configParam(request)
    searchName = post.get('name')
    if searchName:
        param.update(name={'$regex': searchName})
    data = Model.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)

    return render(request, 'admin/company/index.html', {
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
    })

# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        company = Model.objects.filter(name=param.get('name')).order_by("id")
        if company:
            returnData = {'code': '902', 'msg': '公司名已存在', 'data': ''}
        else:
            try:
                model = Model.objects.create(**param)
                if model:
                    returnData = {'code': '200', 'msg': '操作成功', 'data': str(model['id'])}
                else:
                    returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
            except Exception:
                returnData = {'code': '900', 'msg': '数据验证错误', 'data': Exception}
    else:
        returnData = {'code': '901', 'msg': '数据错误', 'data': ''}
    return returnData

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
        param = {
            'name': post.get('name').strip(),
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
                'table': 'company',
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
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if model:
            # 操作成功添加log操作记录
            for id in selection:
                # log记录参数
                logParam = {
                    'table': 'company',
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
    else:
        returnData = {'code': '1000', 'msg': '不允许直接访问', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")

@csrf_exempt
@auth  # 引用登录权限验证
def companylist(request):
    post = request.POST
    returnFormat = post.get('returnFormat')
    data = {}
    model = Model.objects.filter(status=1).order_by("id")
    if model:
        for list in model:
            data[str(list.id)] = list.name
        returnData = {'code': '200', 'msg': '操作成功', 'data': data}
    else:
        returnData = {'code': '200', 'msg': '暂无数据', 'data': data}

    if returnFormat:
        return returnData.get('data')
    elif request.method == 'POST':
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        return returnData.get('data')

# 删除操作
@auth  # 引用登录权限验证
def delete(request):
    post = request.POST
    if post:
        selection = post.getlist('selection[]')
        try:
            model = Model.objects.filter(id__in=selection).delete()
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if model:
            App.objects.filter(companyId__in=selection).delete()
            CreditRule.objects.filter(companyId__in=selection).delete()
            Contract.objects.filter(cid__in=selection).delete()
            # 操作成功添加log操作记录
            for id in selection:
                # log记录参数
                logParam = {
                    'table': 'company',
                    'after': {},
                    'tableId': id,
                }
                logParam.update(action=5)  # log记录参数,action=5为删除
                logsform(request, logParam)
            returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
    else:
        returnData = {'code': '1000', 'msg': '不允许直接访问', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")