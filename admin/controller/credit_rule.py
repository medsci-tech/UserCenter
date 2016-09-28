# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.CreditRule import CreditRule
from admin.controller.app import applist

'''
迈豆积分列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    get = request.GET
    param = {}
    # 获取所有启用应用列表
    app_list = applist(request)
    # 获取配置列表
    cfg_param = configParam(request)
    status_list = cfg_param.get('c_status')
    cycle_list = cfg_param.get('c_cycle')
    searchAppId = get.get('appId')
    selectData = get
    if searchAppId:
        param.update(appId=searchAppId)
    else:
        dataOne = CreditRule.objects.filter(appId__in=app_list.keys()).order_by('id')[:1]  # 获取第一条数据
        if dataOne:
            param.update(appId=dataOne[0]['appId'])
            selectData = dataOne[0]
    data = CreditRule.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表
    # 增强文字可读性
    if data:
        for val in data:
            val.update(statusName=status_list.get(val['status']))
            val.update(cycleName=cycle_list.get(val['cycle']))
    limit = cfg_param.get('c_page')  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        list = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    # return HttpResponse(credit_list)
    return render(request, 'admin/credit_rule/index.html', {
        'list': list,
        'ctrlList': selectData,
        'appList': app_list,
    })

# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = CreditRule.objects.create(**param)
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
            model = CreditRule.objects.get(id=id).update(**param)
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
        extend_list = {}
        # 获取配置列表
        cfg_param = configParam(request)
        ext_credit_list = cfg_param.get('c_ext_credit')
        for key in ext_credit_list:
            if post.get('extend[' + key + ']'):
                extend_list[str(key)] = post.get('extend[' + key + ']')
        param = {
            'appId': post.get('appId'),
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

        return HttpResponse(json.dumps(returnData), content_type="application/json")
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
            model = CreditRule.objects.filter(id__in=selection).update(**param)
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
