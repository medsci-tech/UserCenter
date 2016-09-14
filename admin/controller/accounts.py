#!/usr/bin/env python
#coding:utf-8
from django.shortcuts import render,render_to_response,HttpResponse
from admin.helper import checkcode
from io import StringIO,BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
from admin.model.Admin import Admin
import http.cookiejar,json

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
        if session_code.strip().lower() != verycode.lower():
            return HttpResponse(json.dumps({'status': 0, 'msg': '验证码不匹配!'}))
        else:
            '''验证用户密码'''
            model = Admin.objects.get(username=username)
            return HttpResponse(json.dumps({'status': 0, 'msg':model.username}))
            dj_ps = make_password(password, None, 'pbkdf2_sha256')
            ps_bool = check_password(password, dj_ps)  # check_password 返回值为一个Bool类型，验证密码的正确与否


            return HttpResponse(json.dumps({'status': 0, 'msg': '账户不存在!'}))
    return render(request, 'admin/login.html', {'question': 1})
    #return render_to_response('/admin/login.html',{'error':"",'username':'','pwd':'' })

'''
注销登录
Author : lxhui
Create : 2016-09-12
'''
def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return render(request, 'admin/login.html')