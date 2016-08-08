# coding:utf-8
# 管理员管理
# zhaiyu
from django.shortcuts import render
from users.models import User
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')
