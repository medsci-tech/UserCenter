# coding:utf-8
# 扩展基础管理

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from admin.model.CreditRule import CreditRule
from admin.model.Credit import Credit
from admin.controller.app import applist
from admin.controller.credit import creditlist
from UserCenter.global_templates import configParam
import json

'''
迈豆积分列表
'''
@csrf_exempt
def index(request):
    get = request.GET
    param = {}
    # 获取所有状态列表
    cfg_param = configParam(request)
    status_list = cfg_param.get('c_status')
    cycle_list = cfg_param.get('c_cycle')
    searchAppId = get.get('appId')
    selectData = get
    if searchAppId:
        param.update(appId=searchAppId)
    else:
        dataOne = Credit.objects.all().order_by('id')[:1]  # 获取第一条数据
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
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

    # 获取所有启用应用列表
    app_list = applist('data')
    # 获取所有启用扩展列表
    credit_list = creditlist(selectData['appId'], 'data')
    # return HttpResponse(credit_list)
    return render(request, 'admin/credit_rule/index.html', {
        'topics': topics,
        'request': selectData,
        'appList': app_list,
        'creditList': credit_list,
    })

# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = CreditRule.objects.create(**param)
            if model:
                returnData = {'code': '200', 'msg': '操作成功', 'data': str(model)}
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
@csrf_exempt
def form(request):
    post = request.POST
    id = post.get('id')
    param = {
        'appId': post.get('appId'),
        'credit': post.get('credit'),
        'name': post.get('name'),
        'cycle': post.get('cycle'),
        'rewardNum': post.get('rewardNum'),
        'extends': post.get('extends'),
        'status': post.get('status'),
    }
    if id:
        # 修改
        param.update(id=id)
        returnData = _editById(**param)
    else:
        # 添加
        returnData = _add(**param)

    return HttpResponse(json.dumps(returnData), content_type="application/json")

# 更改状态操作
@csrf_exempt
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
        model = CreditRule.objects.filter(id__in=selection).update(**param)
        if model:
            returnData = {'code': '200', 'msg': '操作成功', 'data': model}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': model}
    except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}

    return HttpResponse(json.dumps(returnData), content_type="application/json")
