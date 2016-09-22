# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.Credit import Credit
from admin.controller.app import applist

'''
迈豆积分列表
'''
@csrf_exempt
@auth  # 引用登录权限验证
def index(request):
    get = request.GET
    param = {}
    # 获取所有启用应用列表
    apps = applist(request)
    # 获取所有状态列表
    cfg_param = configParam(request)
    status_list = cfg_param.get('c_status')
    credit_list = cfg_param.get('c_ext_credit')
    searchAppId = get.get('appId')
    if searchAppId:
        param.update(appId=searchAppId)
    else:
        dataOne = Credit.objects.all().order_by('id')[:1]  # 获取第一条数据
        if dataOne:
            param.update(appId=dataOne[0]['appId'])
    data = Credit.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表
    # 增强文字可读性
    if data:
        for val in data:
            val.update(statusName=status_list.get(val['status']))
            val.update(creditName=credit_list.get(val['credit']))
        selectData = data[0]
    else:
        selectData = get
    limit = cfg_param.get('c_page')  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

    # return HttpResponse(dataOne['id'])
    return render(request, 'admin/credit/index.html', {'topics': topics, 'ctrlList': selectData, 'appList': apps})

# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = Credit.objects.create(**param)
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
            model = Credit.objects.get(id=id).update(**param)
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
    id = post.get('id')
    param = {
        'appId': post.get('appId'),
        'credit': post.get('credit'),
        'name': post.get('name'),
        'icon': post.get('icon'),
        'initNum': post.get('initNum'),
        'ratio': post.get('ratio'),
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
            'table': 'credit',
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

# 更改状态操作
@auth  # 引用登录权限验证
def stats(request):
    post = request.POST
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
        model = Credit.objects.filter(id__in=selection).update(**param)
        if model:
            returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
    except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

'''
根据条件获取启用的积分扩展列表
'''
@auth  # 引用登录权限验证
def creditlist(request):
    post = request.POST
    returnFormat = post.get('returnFormat')
    appId = post.get('appId')
    data = {}
    app = Credit.objects.filter(appId=appId, status=1).order_by("id")
    if app:
        for list in app:
            data[str(list.credit)] = list.name
        returnData = {'code': '200', 'msg': '操作成功', 'data': data}
    else:
        returnData = {'code': '200', 'msg': '暂无数据', 'data': data}

    if returnFormat:
        return returnData.get('data')
    elif request.method == 'POST':
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        return returnData.get('data')