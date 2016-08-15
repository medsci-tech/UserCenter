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

# 修改操作
@csrf_exempt
def form(request):
    post = request.POST
    if post['password']:
        password_mw = post['password']
    else:
        password_mw = '123456'
    param = {
        'username': post['username'],
        'password': make_password(password_mw, None, 'pbkdf2_sha256'),
        'email': post['email'],
        'status': post['status'],
    }
    try:
        Admin(**param).add(**param)
        returnData = {'code': '200', 'msg': 'success', 'data': ''}
    except Exception as e:
        returnData = {'code': '800', 'msg': e, 'data': ''}

    return HttpResponse(json.dumps(returnData), content_type="application/json")
