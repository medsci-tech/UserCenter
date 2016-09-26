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
    get = request.GET
    param = {}
    admin_all_list = {}
    adminId = []
    # 获取所有状态列表
    cfg_param = configParam(request)
    logs_operate = cfg_param.get('c_logs_operate')
    adminAllList = Admin.objects.all().order_by('id')
    for ids in adminAllList:
        admin_all_list[str(ids['id'])] = ids['username']
    table = get.get('table')
    action = get.get('action')
    username = get.get('username')
    if table:
        param.update(table=table)
    if action:
        param.update(action=action)
    if username:
        adminList = Admin.objects.filter(username={'$regex': username}).order_by('id')
        # 将app列表的id作为积分的查询条件
        if adminList:
            for ids in adminList:
                adminId.append(str(ids['id']))
            param.update(adminId__in=adminId)
        else:
            param.update(id='00000000000000000000000a')  # 无效的24位id
    data = Model.objects.filter(**param).order_by("id")  # 根据条件查询积分配置列表
    # 增强文字可读性
    if data:
        for val in data:
            val.update(actionName=logs_operate.get(val['action']))
            val.update(adminName=admin_all_list.get(val['adminId']))
    limit = cfg_param.get('c_page')  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录

    # return HttpResponse(dataOne['id'])
    return render(request, 'admin/logs/index.html', {'topics': topics})


'''
添加log记录--用于controller之间的调用，外部url不能直接访问
    param = {
        'table': 'table',
        'tableId': 'tableId',
        'action': 'action',
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
    try:
        model = Model.objects.create(**param)
        if model:
            returnData = {'code': '200', 'msg': '操作成功', 'data': str(model['id'])}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
    except Exception:
        returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}


    return returnData
