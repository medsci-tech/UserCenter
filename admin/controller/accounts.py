#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse
from admin.helper import checkcode
from io import StringIO,BytesIO
import http.cookiejar

def captcha(request):
    mstream = BytesIO()
    validate_code = checkcode.create_validata_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    #将验证码保存到session
    request.session["CheckCode"] = validate_code[1]  
    return HttpResponse(mstream.getvalue())


'''
系统首页
Author : lxhui
Create : 2016-08-19
'''
def index(request):
    return render(request, 'admin/index.html')

'''
系统登录
Author : lxhui
Create : 2016-08-19
'''
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        check_code = request.POST.get('checkcode')
        #从session中获取验证码
        session_code = request.session["CheckCode"]
        if check_code.strip().lower() != session_code.lower():
            return HttpResponse('验证码不匹配')
        else:
            return HttpResponse('验证码正确')          
    return render(request, 'admin/login.html', {'question': 1})  
    #return render_to_response('/admin/login.html',{'error':"",'username':'','pwd':'' })