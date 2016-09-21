#_*_coding:utf-8_*_
# 管理员管理
__author__ = 'lxhui'

from django.shortcuts import render,render_to_response,HttpResponse
from admin.model.Admin import Admin
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from datetime import *
import json
from admin.controller.auth import *

'''
管理员列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def list(request):
    post = request.POST
    username = post.get('username','').strip()
    nickname = post.get('nickname','').strip()
    email = post.get('email','').strip()
    data = Admin.objects.filter(username__icontains=username,email__icontains=email,nickname__icontains=nickname ).order_by('id')
    limit = 2  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except (EmptyPage, InvalidPage):
        topics = paginator.page(paginator.num_pages)  # 取第一页的记录

    return render(request, 'admin/admin/index.html',{'list':topics,'post': post})

'''
保存管理员
'''
@auth # 引用登录权限验证
def save(request, **param):
    post = request.POST
    if request.method == 'POST':
        model = Admin()
        param = {
            'id': post.get('id'),  # objectid
            'username':post.get('username'), # 用户名
            'password': make_password(post.get('pwd', '123456'), None, 'pbkdf2_sha256'), # 加密,
            'nickname':post.get('nickname', None),  # 昵称
            'email': post.get('email'),  # 邮箱
            'status': post.get('status', 1)  # 状态
        }
        id = param.get('id',0)
        param.pop('id') # 剔除主键
        json_str = model.checkUsername(username=param.get('username',None))
        try:
            decoded = json.loads(json_str)
            if(not id): # 添加操作
                if(not decoded['status']): # 如果用户存在
                    return HttpResponse(json_str)
                else:
                    Admin.objects.create(**param)
                    return HttpResponse(json_str)
            else: # 更新
                if(not post.get('pwd')): # 密码为空则不修改密码
                    param.pop('password')
                Admin.objects.filter(id=id).update(**param)
                return HttpResponse(json.dumps({'status': 1, 'msg': '修改成功!'}))
        except (ValueError, KeyError, TypeError):
            return HttpResponse(json.dumps({'status': 0,'msg':'json格式错误!'}))


def detail(request, question_id):
    pass
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'admin/admin/detail.html', {'question': question})

'''
保存管理员
'''
@auth # 引用登录权限验证
def updateStatus(request, **param):
    post = request.POST
    selection = post.getlist('selection[]')
    status = post.get('status')
    param = {
        'status': status,
    }
    try:
        model = Admin.objects.filter(pk__in=selection).update(**param)
        if model:
            returnData = {'status':1, 'msg': '操作成功!'}
        else:
            returnData = {'status': '0', 'msg': '操作失败!'}
    except Exception:
            returnData = {'code': '0', 'msg': '非法请求!'}

    return HttpResponse(json.dumps(returnData))

