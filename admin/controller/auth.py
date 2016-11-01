#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
def login(request):
    uid = request.session.get('uid', False)
    username = request.session.get('uid', False)
    if uid and username:
        return True
    else:
        return False

def auth(func):
    def inner(request,*arg, **kwargs):
        is_login = login(request)
        if not is_login:
            return HttpResponseRedirect('/admin/login')  # 跳转到登录界面
        temp = func(request,*arg,**kwargs)
        return temp
    return inner