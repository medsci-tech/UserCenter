# -*- coding: utf-8 -*-

from api.controller.common_import import *  # 公共引入文件

from admin.model.BeanLog import BeanLog as Model
# 时间模块
import datetime
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
    if not request_project_id:
        return ApiResponse(-2, '参数错误').json_response()
    try:
        project_data = Model.objects.filter(project_id=request_project_id).aggregate({'$group': {
            '_id': "$rule_type_name",
            'total': {'$sum': '$save_beans'}
        }})
    except:
        return ApiResponse(-2, '参数错误').json_response()
    if project_data:
        return ApiResponse(200, 'success', list(project_data)).json_response()
    else:
        return ApiResponse(200, 'no data').json_response()


# ============================
# 每种规则类型下, 每种策略的迈豆
# ============================
@csrf_exempt
def type_rule(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '错误请求').json_response()
    request_project_id = post.get('project_id')
    request_rule_type_id = post.get('rule_type_id')
    if request_project_id and request_rule_type_id:
        param = {
            'project_id': request_project_id,
            'rule_type_id': request_rule_type_id,
        }
        try:
            project_data = Model.objects.filter(**param).aggregate({'$group': {
                '_id': "$rule_name_ch",
                'total': {'$sum': '$save_beans'}
            }})
        except:
            return ApiResponse(-2, '参数错误').json_response()
        if project_data:
            return ApiResponse(200, 'success', list(project_data)).json_response()
        else:
            return ApiResponse(200, 'no data').json_response()
    else:
        return ApiResponse(-2, '参数错误').json_response()


# ============================
# 每种策略的, 以天为单位每月的迈豆
# ============================
@csrf_exempt
def rule_time(request):
    post = request.POST
    if not post:
        return ApiResponse(403, '错误请求').json_response()
    request_project_id = post.get('project_id')
    request_rule_type_id = post.get('rule_type_id')
    request_start_time = post.get('start_time')
    request_end_time = post.get('end_time')
    if request_project_id and request_rule_type_id:
        param = {
            'project_id': request_project_id,
            'rule_type_id': request_rule_type_id,
        }
        if request_start_time and request_end_time:
            try:
                datetime_start_time = datetime.datetime.strptime(request_start_time, '%Y-%m-%d')
                datetime_end_time = datetime.datetime.strptime(request_end_time, '%Y-%m-%d')
            except Exception:
                # return HttpResponse(param)
                return ApiResponse(-2, '参数错误').json_response()
            if datetime_start_time and datetime_end_time:
                param.update(create_time__gte=datetime_start_time)
                param.update(create_time__lte=datetime_end_time)
        try:
            project_data = Model.objects.filter(**param).aggregate({'$group': {
                '_id': "$rule_name_ch",
                'total': {'$sum': '$save_beans'}
            }})
        except:
            return ApiResponse(-2, '参数错误').json_response()
        if project_data:
            return ApiResponse(200, 'success', list(project_data)).json_response()
        else:
            return ApiResponse(200, 'no data').json_response()
    else:
        return ApiResponse(-2, '参数错误').json_response()

