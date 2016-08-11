# coding:utf-8
# 管理员管理
# zhaiyu
from django.shortcuts import render
from users.model.Admin import Admin
from django.http import HttpResponse

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

def index(request):
    param = {'username':'zhaiyu'}
    data = Admin().find(**param)
    # topics = data.count()
    limit = 3  # 每页显示的记录数

    paginator = Paginator(data, limit)  # 实例化一个分页对象

    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'manager/index.html',{'dataList':data,'dataPage':topics})

def add(request):
    param = {'username': 'zhaiyu','password':123456,'email':'123@123.com','status':1}
    # param = (('username' , 'zhaiyu'),('password' , '123456'))
    # param = {'username','zhaiyu','passwor'}
    res = Admin(**param).add(**param)
    return HttpResponse(res)
    # return render(request, 'manager/index.html')
