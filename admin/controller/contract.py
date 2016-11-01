# coding:utf-8
# 管理员管理
__author__ = 'lxhui'
from admin.controller.common_import import *  # 公共引入文件
from admin.model.Project import Project as Model
from admin.model.Company import Company
from admin.model.Application import Application
from admin.model.BeanRule import BeanRule
import math

@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    param = {}
    searchCompanyId = post.get('company_id')
    searchAppId = post.get('app_id')
    searchName = post.get('name_ch')
    searchCode = post.get('contract_code')
    if searchCompanyId:
        param.update(company_id=searchCompanyId)
    if searchAppId:
        param.update(app_id=searchAppId)
    if searchName:
        param.update(name_ch={'$regex': searchName})
    if searchCode:
        param.update(contract_code={'$regex': searchCode})
    data = Model.objects.filter(**param).order_by("id")

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)

    '''企业信息'''
    comList = Company.objects.filter(status=1).order_by("id")
    if searchCompanyId:
        appList = Application.objects.filter(status=1, company_id=searchCompanyId).order_by("id")
    else:
        appList ={}
    return render(request, 'admin/contract/index.html',{
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
        'comList': comList,
        'appList': appList,
    })


# 添加操作--protected
def _add(**param):
    id = param.get('id')
    if not id:
        try:
            model = Model.objects.create(**param)
        except Exception:
            return ApiResponse(-3, '数据验证错误').json_return()
        if model:
            return ApiResponse(200, '操作成功', str(model['id'])).json_return()
        else:
            return ApiResponse(-1, '操作失败').json_return()
    else:
        return ApiResponse(-2, '数据错误').json_return()


# 修改操作--protected
def _editById(**param):
    id = param.get('id')
    if id:
        try:
            model = Model.objects.get(id=id).update(**param)
        except Exception:
            return ApiResponse(-2, '数据验证错误').json_return()
        if model:
            return ApiResponse(200, '操作成功').json_return()
        else:
            return ApiResponse(-1, 'model操作失败').json_return()
    else:
        return ApiResponse(-2, '数据错误').json_return()


'''
保存合同信息
'''
@auth # 引用登录权限验证
def save(request):
    post = request.POST
    if request.method == 'POST':
        id = post.get('id')  # objectid
        amount = post.get('contract_amount').strip()
        number = post.get('contract_rate').strip()
        totalBeans = math.ceil(float(amount) * float(number))
        param = {
            'company_id': post.get('company_id'),  # 企业id
            'app_id': post.get('app_id'),  # 企业id
            'name_ch':post.get('name_ch'),  # 合同名
            'contract_code': post.get('contract_code'),  # 合同编号
            'contract_amount': amount,  # 合同金额
            'contract_rate': number,  # 合同比例
            'total_beans': totalBeans,  # 总迈豆
            'contract_img': post.get('contract_img'),  # 合同照片
            'start_time': post.get('start_time'),  # 合同有效期
            'end_time': post.get('end_time'),  # 合同截止日期
            'status': post.get('status')  # 状态
        }

        if id:
            # 修改
            param.update(id=id)
            returnData = _editById(**param)
        else:
            # 添加
            returnData = _add(**param)

        # 操作成功添加log操作记录
        if json.loads(returnData).get('code') == 200:
            # log记录参数
            logParam = {
                'table': 'contract',
                'after': param,
            }
            if id:
                logParam.update(table_id=id)  # log记录参数
                logParam.update(action=2)  # log记录参数,rule_name_en=2为修改
            else:
                logParam.update(table_id=json.loads(returnData).get('data'))  # log记录参数
                logParam.update(action=1)  # log记录参数,rule_name_en=1为添加
            if 'id' in logParam['after']:
                del logParam['after']['id']
            logsform(request, logParam)
        return HttpResponse(returnData, content_type="application/json")
    else:
        return ApiResponse(403, '不允许直接访问').json_response()


'''
充值
'''
@auth # 引用登录权限验证
def recharge(request):
    post = request.POST
    if request.method == 'POST':
        id = post.get('id')
        request_amount = post.get('contract_amount').strip()
        try:
            contractData = Model.objects.get(id=id)
        except:
            return ApiResponse(-1, '参数错误').json_response()
        if not contractData:
            return ApiResponse(-1, '参数错误').json_response()
        save_amount = float(request_amount) + float(contractData['contract_amount'])
        totalBeans = math.ceil(save_amount * float(contractData['contract_rate']))
        param = {
            'id': id,
            'contract_amount': save_amount,  # 合同金额
            'total_beans': totalBeans,  # 总迈豆
        }
        returnData = _editById(**param)

        # return HttpResponse(returnData, content_type="application/json")
        if json.loads(returnData).get('code') == 200:
            # log记录参数
            logParam = {
                'table': 'contract',
                'after': param,
                'table_id': id,
                'action': 6,
            }
            logsform(request, logParam)
        return HttpResponse(returnData, content_type="application/json")
    else:
        return ApiResponse(403, '不允许直接访问').json_response()


'''
更新状态
'''
@auth # 引用登录权限验证
def updateStatus(request, **param):
    post = request.POST
    selection = post.getlist('selection[]')
    status = post.get('status')
    param = {
        'status': status,
    }
    try:
        #model = Model.objects.filter(pk__in=selection).delete() # 删除
        model = Model.objects.filter(pk__in=selection).update(**param)
        if model:
            return ApiResponse(200, '操作成功').json_response()
        else:
            return ApiResponse(-1, '操作失败').json_response()
    except Exception:
            return ApiResponse(-2, '非法请求').json_response()

# 删除操作
@auth  # 引用登录权限验证
def delete(request):
    post = request.POST
    if post:
        selection = post.getlist('selection[]')
        try:
            model = Model.objects.filter(id__in=selection).delete()
        except Exception:
            return ApiResponse(-2, '数据验证错误').json_response()
        if model:
            BeanRule.objects.filter(contractId__in=selection).delete()
            # 操作成功添加log操作记录
            for id in selection:
                # log记录参数
                logParam = {
                    'table': 'company',
                    'after': {},
                    'table_id': id,
                }
                logParam.update(action=5)  # log记录参数,rule_name_en=5为删除
                logsform(request, logParam)
            return ApiResponse(200, '操作成功').json_response()
        else:
            return ApiResponse(-1, '操作失败').json_response()
    else:
        return ApiResponse(403, '不允许直接访问').json_response()

'''
前端访问接口
'''
@auth  # 引用登录权限验证
def contractlist(request, **kwargs):
    if request.method == 'POST':
        req = request.POST
        appId = req.get('app_id')
    else:
        appId = kwargs.get('app_id')
    returnFormat = kwargs.get('returnFormat')
    data = {}
    if appId:
        try:
            modelData = Model.objects.filter(status=1, appId=appId).order_by("id")
        except Exception:
            modelData = {}
        if modelData:
            for val in modelData:
                data[str(val.id)] = val.name
        if data:
            returnData = ApiResponse(200, '操作成功', data).json_return()
        else:
            returnData = ApiResponse(200, '暂无数据', data).json_return()
    else:
        returnData = ApiResponse(200, '参数缺失').json_return()

    if returnFormat:
        return data
    elif request.method == 'POST':
        return HttpResponse(returnData, content_type="application/json")
    else:
        return data
