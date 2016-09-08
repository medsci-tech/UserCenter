# coding:utf-8
# 扩展基础管理

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from admin.model.Extcredits import Extcredits
from admin.model.App import App
from admin.controller.app import applist
from UserCenter.global_templates import configParam
import json

'''
迈豆积分列表
'''
@csrf_exempt
def index(request):
    post = request.POST
    param = {}
    # 获取所有启用应用列表
    apps = applist('data')
    # 获取所有状态列表
    cfg_param = configParam(request)
    status_list = cfg_param.get('c_status')
    if request.method == "POST":
        searchAppId = post.get('appId')
        param.update(appId=searchAppId)
    else:
        dataOne = Extcredits.objects.all().order_by('id')[:1]  # 获取第一条数据
        if dataOne:
            param.update(appId=dataOne[0]['appId'])
    data = Extcredits.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表
    # 增强文字可读性
    if data:
        for val in data:
            val.update(statusName=status_list.get(val['status']))
        selectData = data[0]
    else:
        selectData = post
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
    return render(request, 'admin/extcredits/index.html', {'topics': topics, 'request': selectData, 'appList': apps})

# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = Extcredits.objects.create(**param)
            if model:
                returnData = {'code': '200', 'msg': '操作成功', 'data': str(model)}
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
            model = Extcredits.objects.get(id=id).update(**param)
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
        model = Extcredits.objects.filter(id__in=selection).update(**param)
        if model:
            returnData = {'code': '200', 'msg': '操作成功', 'data': model}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': model}
    except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': Exception}

    return HttpResponse(json.dumps(returnData), content_type="application/json")
