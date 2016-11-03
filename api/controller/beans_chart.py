# -*- coding: utf-8 -*-

from api.controller.common_import import *  # 公共引入文件

from admin.model.BeanLog import BeanLog as Model
# 时间模块
import datetime
import calendar
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
        project_data = Model.objects.filter(project_id=request_project_id).aggregate(
            {'$group': {
                '_id': {'rule_type_name': '$rule_type_name', 'rule_type_name_en': '$rule_type_name_en'},
                'total': {'$sum': '$save_beans'},
            }},
        )
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
    request_rule_type_name = post.get('rule_type_name')
    if request_project_id and request_rule_type_name:
        param = {
            'project_id': request_project_id,
            'rule_type_name_en': request_rule_type_name,
        }
        try:
            project_data = Model.objects.filter(**param).aggregate({'$group': {
                '_id': {'rule_name_ch': '$rule_name_ch', 'rule_type_name_en': '$rule_type_name_en'},
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
    request_rule_type_name = post.get('rule_type_name')
    request_year = post.get('year')
    request_month = post.get('month')
    if request_project_id and request_rule_type_name:
        param = {
            'project_id': request_project_id,
            'rule_type_name_en': request_rule_type_name,
        }
        if request_year and request_month:
            try:
                datetime_start_time = datetime.datetime.strptime(request_year + '-' + request_month, '%Y-%m')
                days = calendar.monthrange(int(request_year), int(request_month))[1]
                datetime_end_time = datetime_start_time + datetime.timedelta(days=days)
            except:
                return ApiResponse(-2, '参数错误').json_response()
            param.update(create_time__gte=datetime_start_time)
            param.update(create_time__lte=datetime_end_time)
            # return HttpResponse(datetime_start_time)
        else:
            return ApiResponse(-2, '参数错误').json_response()
        try:
            project_data = Model.objects.filter(**param).aggregate(
                {'$group': {
                    '_id': {
                        'rule_name': '$rule_name_ch',
                        'day': {'$dayOfMonth': '$create_time'},
                    },
                    'total': {'$sum': '$save_beans'},
                }},
                {'$sort': {'_id': 1}},
            )
        except:
            return ApiResponse(-2, '参数错误e').json_response()
        if project_data:
            return ApiResponse(200, 'success', list(project_data)).json_response()
        else:
            return ApiResponse(200, 'no data').json_response()
    else:
        return ApiResponse(-2, '参数错误').json_response()

