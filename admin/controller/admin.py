# coding:utf-8
'''
系统管理入口
author:lxhui
'''
from django.shortcuts import render
#from admin.model.Admin import Admin
from django.http import HttpResponse

'''
系统首页
'''
def index(request):
    return render(request, 'admin/index.html')

'''
系统登录
'''
def login(request):
    #return HttpResponse('test')
    return render(request, 'admin/login.html', {'question': 1})
