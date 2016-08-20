# coding:utf-8
# 管理员管理
# zhaiyu
from django.shortcuts import render
from users.model.Admin import Admin
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json
from mongoengine import *
from django.db import transaction
from bson.objectid import ObjectId

def index(request):
    param = {}
    data = Admin().find(**param)
    limit = 20  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'admin/index.html',{'topics':topics})

# 添加操作
def _add(**param):
    id = param.get('id')
    password = param.get('password')
    if not id:
        if not password:
            password = '123456'
        param.update(password=make_password(password, None, 'pbkdf2_sha256'))
        try:
            model = Admin(**param).add(**param)
            if model:
                returnData = {'code': '200', 'msg': '操作成功', 'data': str(model)}
            else:
                returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}
    else:
        returnData = {'code': '901', 'msg': '数据错误', 'data': ''}
    return returnData

# 修改操作
def _editById(**param):
    id = param.get('id')
    password = param.get('password')
    if id:
        if hasattr(param, 'password'):
            if password:
                param.update(password=make_password(password, None, 'pbkdf2_sha256'))
            else:
                param.pop('password')
        try:
            model = Admin(**param).editById(**param)
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
def form(request):
    post = request.POST
    id = post['id']
    param = {
        'username': post['username'],
        'nickname': post['nickname'],
        'password': post['password'],
        'email': post['email'],
        'status': post['status'],
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
        status = '1'
    else:
        status = '0'
    param = {
        'selection':selection,
        'status': status,
    }
    res = Admin(**param).editByFilter(**param)
    # try:
    #     for id in selection:
    #         param.update(id=id)
    #         Admin(**param).editById(**param)
    #     returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
    # except Exception:
    #     transaction.rollback()
    #     returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
    # returnData = {'code': '801', 'msg': '操作失败', 'data': ''}

    # returnData = _editById(**param)

    return HttpResponse(res)
    # return HttpResponse(json.dumps(returnData), content_type="application/json")
