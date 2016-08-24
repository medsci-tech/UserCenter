# coding:utf8
from django.shortcuts import render,render_to_response,HttpResponse
from mongoengine import *
'''
系统权限控制基类
Author : lxhui
Create : 2016-08-20
'''
class Auth(Document):
        meta = {  
        'allow_inheritance': True,  
     }
        '登录权限验证'
        def __init__(self):
                return HttpResponse('no access')
                #return render(request, 'admin/detail.html', {'question': question})
                
                               
if __name__ == "__main__":  
    Auth()  

        
        
    