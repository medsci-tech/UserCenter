# coding:utf8
from django.shortcuts import render,render_to_response,HttpResponse,HttpResponseRedirect
from mongoengine import *
'''
系统权限控制基类
Author : lxhui
Create : 2016-08-20
'''
class Auth(Document):
        meta = { 'allow_inheritance': True, 'abstract': True }# 允许继承          
        def check_permissions(self):
                return 1
        '登录权限验证'

        def __init__(self, *args, **kwargs):
                super(Document, self).__init__(self, *args, **kwargs)
                #Document.__init__(self)
                self.check_permissions()
                return None

        #def __init__(self):
                #return HttpResponse('no access')
                #return render(request, 'admin/detail.html', {'question': question})
        def test(self):
                return 'a'

if __name__ == "__main__":  
        Auth()

