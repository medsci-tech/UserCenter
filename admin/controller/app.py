#_*_coding:utf-8_*_
# 应用平台管理

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

from admin.model.App import App
from UserCenter.global_templates import configParam
import json

@csrf_exempt
def index(request):
    post = request.POST
    param = {}
    # 获取所有状态列表
    cfg_param = configParam(request)
    status_list = cfg_param.get('c_status')
    if request.method == "POST":
        name = post.get('name').strip()
        if name:
            param.update(name={'$regex': name})
    data = App.objects.filter(**param).order_by("id")
    # 增强文字可读性
    for val in data:
        val.update(statusName=status_list.get(val['status']))
    limit = 20  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'admin/app/index.html',{'topics':topics, 'ctrlList': post})

 
 
# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = App.objects.create(**param)
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
            model = App.objects.get(id=id).update(**param)
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
def form(request):
    post = request.POST
    id = post.get('id')
    param = {
        'name': post.get('name'),
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

    return HttpResponse(json.dumps(returnData), content_type="application/json")

# 更改状态操作
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
        model = App.objects.filter(id__in=selection).update(**param)
        if model:
            returnData = {'code': '200', 'msg': '操作成功', 'data': model}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': model}
    except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

@csrf_exempt
def applist(request):
    post = request.POST
    returnFormat = post.get('returnFormat')
    data = {}
    app = App.objects.filter(status=1).order_by("id")
    if app:
        for list in app:
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