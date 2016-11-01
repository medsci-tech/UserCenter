# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *

from django.contrib.auth.hashers import make_password
from admin.model.User import User as Model
from admin.model.Project import Project
import datetime
'''
迈豆积分列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    param = {}
    # 获取配置列表
    searchRole = post.get('role')
    searchPhone = post.get('phone')
    if searchRole:
        param.update(role=searchRole)
    if searchPhone:
        param.update(phone=searchPhone)
    data = Model.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)

    try:
        contratcData = Project.objects.filter(status=1).order_by("id")
    except:
        contratcData = {}
    return render(request, 'admin/user/index.html', {
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
        'list_contratcData': contratcData,
    })

# 添加操作--protected
def _add(**param):
    id = param.get('id')
    phone = param.get('phone')
    password = param.get('password')
    if not id:
        try:
            check_model = Model.objects.get(phone=phone)
        except:
            check_model = None
        if check_model:
            return ApiResponse(-4, '手机号已经存在').json_return()
        if not password:
            # 如果没有填密码则为默认密码
            password = '123456'
        param.update(password=make_password(password, None, 'pbkdf2_sha256'))
        try:
            model = Model.objects.create(**param)
            return ApiResponse(200, '操作成功', str(model['id'])).json_return()
        except Exception:
            return ApiResponse(-3, '数据验证错误').json_return()
    else:
        return ApiResponse(-1, '数据错误').json_return()

# 修改操作--protected
def _editById(**param):
    id = param.get('id')
    phone = param.get('phone')
    password = param.get('password')
    if id:
        try:
            check_model = Model.objects.get(phone=phone)
        except:
            check_model = None
        if check_model and str(check_model['id']) != id:
            return ApiResponse(-4, '手机号已经存在').json_return()
        if hasattr(param, 'password'):
            if password:
                param.update(password=make_password(password, None, 'pbkdf2_sha256'))
            else:
                # 如果留空则移除password属性，不修改密码
                param.pop('password')
        try:
            # param.update(updated_at=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            Model.objects.get(id=id).update(**param)
            return ApiResponse(200, '操作成功').json_return()
        except Exception:
            return ApiResponse(-3, '数据错误').json_return()
    else:
        return ApiResponse(-1, '数据错误').json_return()

# 修改操作
@auth  # 引用登录权限验证
def form(request):
    post = request.POST
    if post:
        id = post.get('id')
        phone = post.get('phone')
        param = {
            'phone': phone,
            'password': post.get('password'),
            'role': post.get('role'),
            'province': post.get('province'),
            'city': post.get('city'),
            'district': post.get('district'),
        }
        if id:
            # 修改
            param.update(id=id)
            returnData = _editById(**param)
        else:
            # 添加
            returnData = _add(**param)

        # 操作成功添加log操作记录
        if json.loads(returnData).get('code') == 200:
            # log记录参数
            logParam = {
                'table': 'credit_rule',
                'after': param,
            }
            if id:
                logParam.update(table_id=id)  # log记录参数
                logParam.update(action=2)  # log记录参数,rule_name_en=2为修改
            else:
                logParam.update(table_id=returnData.get('data'))  # log记录参数
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
                    'table': 'credit_rule',
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
