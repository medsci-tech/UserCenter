# -*- coding: utf-8 -*-

from api.controller.common_import import *  # 公共引入文件

from admin.model.BeanLog import BeanLog as Model
# 时间模块
import datetime
import math

'''
    积分图表接口
'''


# ============================
# 每个项目下, 每种规则类型的迈豆
# ============================
@csrf_exempt
def project_type(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '错误请求').json_response()
    request_project_id = post.get('project_id')
    try:
        project_data = Model.objects.filter(project_id=request_project_id).order_by('id')
    except:
        return ApiResponse(-5, '记录查询错误').json_response()


# ============================
# 每种规则类型下, 每种策略的迈豆
# ============================
@csrf_exempt
def type_rule(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '错误请求').json_response()



# ============================
# 每种策略的, 以天为单位每月的迈豆
# ============================
@csrf_exempt
def rule_time(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '错误请求').json_response()

