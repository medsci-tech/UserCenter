# 模板
# coding:utf-8
from django.shortcuts import render
from users.models import User
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'login.html')
def tables(request):
    return render(request, 'tables.html')

def testdb(request):
    res = User().find(likes=100)
    #res = User().add(name="test3")
    return HttpResponse(res)

