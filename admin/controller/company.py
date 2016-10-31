# -*- coding: utf-8 -*-
# 企业管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.Company import Company as Model
from admin.model.Application import Application
from admin.model.BeanRule import BeanRule
from admin.model.Project import Project

'''
迈豆积分列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    param = {}
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
            return ApiResponse(-3, '公司名已存在').json_return()
        else:
            try:
                model = Model.objects.create(**param)
                if model:
                    return ApiResponse(200, '操作成功', str(model['id'])).json_return()
                else:
                    return ApiResponse(-1, '操作失败').json_return()
            except Exception:
                return ApiResponse(-1, '数据验证错误').json_return()
    else:
        return ApiResponse(-1, '数据错误').json_return()

# 修改操作--protected
def _editById(**param):
    id = param.get('id')
    if id:
        try:
            model = Model.objects.get(id=id).update(**param)
            if model:
                return ApiResponse(200, '操作成功').json_return()
            else:
                return ApiResponse(-1, '操作失败').json_return()
        except Exception:
            return ApiResponse(-3, '数据验证错误').json_return()
    else:
        return ApiResponse(-2, '数据错误').json_return()


# 修改操作
@auth  # 引用登录权限验证
def form(request):
    post = request.POST
    if post:
        id = post.get('id')
        param = {
            'name': post.get('name'),
            'status': post.get('status'),
        }
        if id:
            # 修改
            param.update(id=id)
            returnData = _editById(**param)
        else:
            # 添加
            returnData = _add(**param)

        # return ApiResponse(403, '不允许直接访问', json.loads(returnData)).json_response()
        # 操作成功添加log操作记录
        if json.loads(returnData).get('code') == '200':
            # log记录参数
            logParam = {
                'table': 'company',
                'after': param,
            }
            if id:
                logParam.update(table_id=id)  # log记录参数
                logParam.update(action=2)  # log记录参数,rule_name_en=2为修改
            else:
                logParam.update(table_id=json.loads(returnData).get('data'))  # log记录参数
                logParam.update(action=1)  # log记录参数,rule_name_en=1为添加
            if 'id' in logParam['after']:
                del logParam['after']['id']
            logsform(request, logParam)
        return HttpResponse(returnData, content_type="application/json")
    else:
        return ApiResponse(403, '不允许直接访问').json_response()

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
            return ApiResponse(-2, '数据验证错误').json_response()
        if model:
            # 操作成功添加log操作记录
            for id in selection:
                # log记录参数
                logParam = {
                    'table': 'company',
                    'after': param,
                    'table_id': id,
                }
                if statusType == 'enable':
                    logParam.update(action=3)  # log记录参数,rule_name_en=3为启用
                else:
                    logParam.update(action=4)  # log记录参数,rule_name_en=4为禁用
                if 'id' in logParam['after']:
                    del logParam['after']['id']
                logsform(request, logParam)

            return ApiResponse(200, '操作成功').json_response()
        else:
            return ApiResponse(-1, '操作失败').json_response()
    else:
        return ApiResponse(403, '不允许直接访问').json_response()


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
        returnData = ApiResponse(200, '操作成功', data).json_return()
    else:
        returnData = ApiResponse(200, '暂无数据', data).json_return()
    if returnFormat:
        return data
    elif request.method == 'POST':
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        return data

# 删除操作
@auth  # 引用登录权限验证
def delete(request):
    post = request.POST
    if post:
        selection = post.getlist('selection[]')
        try:
            model = Model.objects.filter(id__in=selection).delete()
        except Exception:
            return ApiResponse(-3, '数据验证错误').json_response()
        if model:
            Application.objects.filter(companyId__in=selection).delete()
            BeanRule.objects.filter(companyId__in=selection).delete()
            Project.objects.filter(cid__in=selection).delete()
            # 操作成功添加log操作记录
            for id in selection:
                # log记录参数
                logParam = {
                    'table': 'company',
                    'after': {},
                    'table_id': id,
                }
                logParam.update(action=5)  # log记录参数,rule_name_en=5为删除
                logsform(request, logParam)
            return ApiResponse(200, '操作成功').json_response()
        else:
            return ApiResponse(-1, '操作失败').json_response()
    else:
        return ApiResponse(403, '不允许直接访问').json_response()