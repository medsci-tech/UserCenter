# -*- coding: utf-8 -*-
# 应用平台管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.Company import Company
from admin.model.Application import Application as Model
from admin.model.BeanRule import BeanRule
from admin.model.Project import Project

@csrf_exempt
@auth  # 引用登录权限验证
def index(request):
    get = request.GET
    post = request.POST
    param = {}
    # 获取所有状态列表
    searchCompanyId = get.get('company_id')
    searchName = post.get('name')
    if searchCompanyId:
        param.update(company_id=searchCompanyId)
        if searchName:
            param.update(name={'$regex': searchName})
        data = Model.objects.filter(**param).order_by("id")
        companyData = Company.objects.filter(id=searchCompanyId).order_by("id")[:1][0]
    else:
        data = {}
        companyData = {}
    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)
    return render(request, 'admin/app/index.html',{
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
        'form_companyData': companyData,
    })

 
 
# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
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
            return ApiResponse(-1, '数据验证错误').json_return()
    else:
        return ApiResponse(-1, '数据错误').json_return()

# 修改操作
@auth  # 引用登录权限验证
def form(request):
    post = request.POST
    if post:
        id = post.get('id')
        param = {
            'name': post.get('name'),
            'company_id': post.get('company_id'),
            'description': post.get('description'),
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
        if json.loads(returnData).get('code') == '200':
            # log记录参数
            logParam = {
                'table': 'app',
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
            if model:
                # 操作成功添加log操作记录
                for id in selection:
                    # log记录参数
                    logParam = {
                        'table': 'app',
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
        except Exception:
            return ApiResponse(-3, '数据验证错误').json_response()
    else:
        return ApiResponse(403, '不允许直接访问').json_response()
'''
前端访问接口
'''
@auth  # 引用登录权限验证
def applist(request, **kwargs):
    if request.method == 'POST':
        req = request.POST
        companyId = req.get('company_id')
    else:
        companyId = kwargs.get('company_id')
    returnFormat = kwargs.get('returnFormat')
    data = {}
    if companyId:
        try:
            app = Model.objects.filter(status=1, company_id=companyId).order_by("id")
        except Exception:
            app = {}
        if app:
            for val in app:
                data[str(val.id)] = val.name
        if data:
            returnData = ApiResponse(200, '操作成功', data).json_return()
        else:
            returnData = ApiResponse(200, '暂无数据', data).json_return()
    else:
        returnData = ApiResponse(200, '参数缺失').json_return()

    if returnFormat:
        return data
    elif request.method == 'POST':
        return HttpResponse(returnData, content_type="application/json")
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
            returnData = {'contract_code': '900', 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if model:
            BeanRule.objects.filter(app_id__in=selection).delete()
            Project.objects.filter(app_id__in=selection).delete()
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
            returnData = {'contract_code': '200', 'msg': '操作成功', 'data': ''}
        else:
            returnData = {'contract_code': '801', 'msg': '操作失败', 'data': ''}
    else:
        returnData = {'contract_code': '1000', 'msg': '不允许直接访问', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")