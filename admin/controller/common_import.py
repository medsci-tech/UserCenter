# -*- coding: utf-8 -*-
# 公共引入文件

# 输出模板
from django.shortcuts import render
from django.http import HttpResponse

# 分页
from admin.controller.funForMime import paginationForMime

# csrf
from django.views.decorators.csrf import csrf_exempt

# configParam
from UserCenter.global_templates import configParam

# json
import json

# 登录验证
from admin.controller.auth import auth

# 引入log记录方法
from admin.controller.syslog import logsform

# ApiResponse
from helper.apiResponse import ApiResponse

