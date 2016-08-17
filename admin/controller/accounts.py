#!/usr/bin/env python
#coding:utf-8

from django.shortcuts import render,render_to_response,HttpResponse
from admin.helper import checkcode
from io import StringIO
def captcha(request):
    mstream = StringIO()
    
    validate_code = checkcode.create_validata_code()
    img = validate_code[0]
    img.save(mstream, "GIF")
    
    #将验证码保存到session
    request.session["CheckCode"] = validate_code[1]
    
    return HttpResponse(mstream.getvalue()) 
