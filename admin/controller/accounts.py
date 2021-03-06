#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse
from admin.helper import checkcode
from io import StringIO,BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from admin.model.Admin import Admin
from django.core.exceptions import ObjectDoesNotExist
#from django.http import HttpResponseRedirect
import http.cookiejar,json
from admin.controller.auth import *
def captcha(request):
    mstream = BytesIO()
    validate_code = checkcode.create_validata_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    # 将验证码保存到session
    request.session["verycode"] = validate_code[1]
    return HttpResponse(mstream.getvalue())

'''
系统首页
Author : lxhui
Create : 2016-08-19
'''
@auth # 引用登录权限验证
def index(request):
    return render(request, 'admin/index.html')

'''
系统登录
Author : lxhui
Create : 2016-08-19
'''
@csrf_exempt
def login(request):
    if request.method == 'POST':
        post = request.POST
        username = post.get('username') # 用户名
        password = post.get('password') # 密码
        verycode = post.get('verycode') # 验证码
        # 从session中获取验证码
        if request.session.get('uid', False):
            return HttpResponse("You've already logod.")

        session_code = request.session.get('verycode','')
        if session_code.strip().lower() != verycode.strip().lower():
            return HttpResponse(json.dumps({'status': 0, 'msg': '验证码不匹配!'}))
        else:
            try:
                '''验证用户密码'''
                model = Admin.objects.get(username=username)
                if not model:
                    return HttpResponse(json.dumps({'status': 0, 'msg': '用户名不存在!'}))
                else:
                    dj_ps = model.password
                    ps_bool = check_password(password, dj_ps)  # check_password 返回值为一个Bool类型，验证密码的正确与否
                    if not ps_bool:  # 密码验证错误
                        return HttpResponse(json.dumps({'status': 0, 'msg': '密码输入错误!'}))
                    else:  # 验证成功
                        '''记录会话session'''
                        request.session['uid'] = str(model.id)
                        request.session['username'] = model.username
                        return HttpResponse(json.dumps({'status': 1, 'msg': '登录成功!'}))
            except Admin.DoesNotExist:
                return HttpResponse(json.dumps({'status': 0, 'msg': '账号不存在!'}))
    return render(request, 'admin/login.html')
    #return render_to_response('/admin/login.html',{'error':"",'username':'','pwd':'' })

'''
注销登录
Author : lxhui
Create : 2016-09-12
'''
def logout(request):
    try:
        del request.session['uid'],request.session['username']
    except KeyError:
        pass
    return render(request, 'admin/login.html')