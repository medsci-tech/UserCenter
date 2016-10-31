# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *

from admin.model.Syslog import Syslog as Model
from admin.model.Admin import Admin

'''
迈豆积分列表
'''
@csrf_exempt
@auth  # 引用登录权限验证
def index(request):
    post = request.POST
    param = {}
    adminId = []
    table = post.get('table')
    action = post.get('rule_name_en')
    adminName = post.get('admin_name')
    if table:
        param.update(table=table)
    if action:
        param.update(action=action)
    if adminName:
        adminList = Admin.objects.filter(username={'$regex': adminName}).order_by('id')
        # 将app列表的id作为积分的查询条件
        if adminList:
            for ids in adminList:
                adminId.append(str(ids['id']))
            param.update(adminId__in=adminId)
        else:
            param.update(id='00000000000000000000000a')  # 无效的24位id
    data = Model.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)

    return render(request, 'admin/logs/index.html', {
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
    })

'''
添加log记录--用于controller之间的调用，外部url不能直接访问
    param = {
        'table': 'table',
        'table_id': 'table_id',
        'rule_name_en': 'rule_name_en',
        'after': 'after',
    }
'''
def logsform(request, param):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    param.update(ip=ip)
    param.update(adminId=request.session.get('uid'))
    param.update(adminName=request.session.get('username'))
    try:
        model = Model.objects.create(**param)
        if model:
            returnData = {'contract_code': '200', 'msg': '操作成功', 'data': str(model['id'])}
        else:
            returnData = {'contract_code': '801', 'msg': '操作失败', 'data': ''}
    except Exception:
        returnData = {'contract_code': '900', 'msg': '数据验证错误', 'data': ''}

    return returnData
