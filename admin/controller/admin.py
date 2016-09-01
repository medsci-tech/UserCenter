#_*_coding:utf-8_*_
# 管理员管理
__author__ = 'lxhui'

from django.shortcuts import render
from admin.model.Admin import Admin
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
import json

'''
管理员列表
'''
@csrf_exempt
def list(request):
    post = request.POST
   
    list = Admin.objects.all().order_by("id")

    #return HttpResponse(Admin.meta.collection)

    return render(request, 'admin/admin/index.html',{'list':list, 'request': post})


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'admin/admin/detail.html', {'question': question})
 
 
# 添加操作--protected
def _add(**param):
    id = param.get('id')
    password = param.get('password')
    if not id:
        if not password:
            # 如果没有填密码则为默认密码
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

# 修改操作--protected
def _editById(**param):
    id = param.get('id')
    password = param.get('password')
    if id:
        if hasattr(param, 'password'):
            if password:
                param.update(password=make_password(password, None, 'pbkdf2_sha256'))
            else:
                # 如果留空则移除password属性，不修改密码
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
    id = post.get('id')
    param = {
        'username': post.get('username'),
        'nickname': post.get('nickname'),
        'password': post.get('password'),
        'email': post.get('email'),
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
        status = '1'
    else:
        status = '0'
    param = {
        'status': status,
    }

    try:
        model = Admin(**param).editByFilter(selection, **param)
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
