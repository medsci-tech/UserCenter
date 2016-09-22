# coding:utf-8
# 管理员管理
__author__ = 'lxhui'
from django.shortcuts import render
from admin.model.Contract import Contract
from django.http import HttpResponse
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json
from admin.controller.auth import *
@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    name = post.get('name','').strip()
    number = post.get('number','').strip()
    data = Contract.objects.filter(name__icontains=name,number__icontains=number).order_by('id')
    limit = 20  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)
    return render(request, 'admin/contract/index.html',{'list':list, 'request2': post})

# 添加操作--protected
@auth # 引用登录权限验证
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = Contract(**param).add(**param)
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
@auth # 引用登录权限验证
def _editById(**param):
    id = param.get('id')
    img = param.get('img')
    if id:
        if not img:
            # 如果留空则移除img属性，不做修改
            param.pop('img')
        try:
            model = Contract(**param).editById(**param)
            '''
                返回值 model
                nModified:修改成功1，修改失败0
                updatedExisting:根据条件查询结果，有true，无false
                n:根据条件查询结果，有1，无0
                ok:1
            '''
            if model.get('n'):
                if model.get('ok'):
                    returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
                else:
                    returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
            else:
                returnData = {'code': '802', 'msg': '不存在的数据集', 'data': ''}
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}
    else:
        returnData = {'code': '901', 'msg': '数据错误', 'data': ''}
    return returnData

# 修改操作
@csrf_exempt
@auth # 引用登录权限验证
def form(request):
    post = request.POST
    id = post.get('id')
    param = {
        'name': post.get('name'),
        'number': post.get('number'),
        'amount': post.get('amount'),
        'img': post.get('img'),
        'startTime': post.get('startTime'),
        'endTime': post.get('endTime'),
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
@auth # 引用登录权限验证
def stats(request):
    post = request.POST
    selection = post.getlist('selection[]')
    statusType = post.get('statusType')
    if statusType == 'enable':
        status = '1'
    else:
        status = '0'
    param = {
        'status': status,
    }

    try:
        model = Contract(**param).editByIds(selection, **param)
        if model.get('n'):
            if model.get('ok'):
                returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
            else:
                returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
        else:
            returnData = {'code': '802', 'msg': '不存在的数据集', 'data': ''}
    except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

def test(request):
    return render(request, 'admin/common/test.html')