# coding:utf-8
# 管理员管理
__author__ = 'lxhui'
from admin.controller.common_import import *  # 公共引入文件
from admin.model.Contract import Contract as Model
from admin.model.Company import Company
from admin.model.App import App
from admin.model.CreditRule import CreditRule
import math

@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    param = {}
    searchCompanyId = post.get('companyId')
    searchAppId = post.get('appId')
    searchName = post.get('name')
    searchCode = post.get('code')
    if searchCompanyId:
        param.update(companyId=searchCompanyId)
    if searchAppId:
        param.update(appId=searchAppId)
    if searchName:
        param.update(name={'$regex': searchName})
    if searchCode:
        param.update(code={'$regex': searchCode})
    data = Model.objects.filter(**param).order_by("id")

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)

    '''企业信息'''
    comList = Company.objects.filter(status=1).order_by("id")
    if searchCompanyId:
        appList = App.objects.filter(status=1, companyId=searchCompanyId).order_by("id")
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


'''
保存合同信息
'''
@auth # 引用登录权限验证
def save(request):
    post = request.POST
    if request.method == 'POST':
        amount = post.get('amount').strip()
        number = post.get('number').strip()
        totalBeans = math.ceil(float(amount) * float(number))
        param = {
            'id': post.get('id'),  # objectid
            'companyId': post.get('companyId'),  # 企业id
            'appId': post.get('appId'),  # 企业id
            'name':post.get('name'),  # 合同名
            'code': post.get('code'),  # 合同编号
            'amount': amount,  # 合同金额
            'number': number,  # 合同比例
            'totalBeans': totalBeans,  # 总迈豆
            'img': post.get('img'),  # 合同照片
            'startTime': post.get('startTime'),  # 合同有效期
            'endTime': post.get('endTime'),  # 合同截止日期
            'status': post.get('status')  # 状态
        }
        id = param.get('id',0)
        param.pop('id') # 剔除主键
        # log记录参数
        logParam = {
            'table': 'contract',
            'after': param,
        }
        try:
            if(not id): # 添加操作
                obj = Model.objects.create(**param)
                logParam.update(tableId=obj.id)  # log记录参数
                logParam.update(action=1)  # log记录参数,action=1为添加
            else: # 更新
                Model.objects.filter(id=id).update(**param)
                logParam.update(tableId=id)  # log记录参数
                logParam.update(action=2)  # log记录参数,action=2为修改

            logsform(request, logParam)
            return HttpResponse(json.dumps({'code': 200, 'msg': '操作成功!'}), content_type="application/json")
        except (ValueError, KeyError, TypeError):
            return HttpResponse(json.dumps({'code': 0,'msg':'json格式错误!'}), content_type="application/json")


'''
充值
'''
@auth # 引用登录权限验证
def recharge(request):
    post = request.POST
    if request.method == 'POST':
        id = post.get('id')
        request_amount = post.get('amount').strip()
        try:
            contractData = Model.objects.get(id=id)
        except:
            return HttpResponse(json.dumps({'code': -1 ,'msg': '参数错误'}), content_type="application/json")
        if not contractData:
            return HttpResponse(json.dumps({'code': -1 ,'msg': '参数错误'}), content_type="application/json")
        save_amount = float(request_amount) + float(contractData['amount'])
        totalBeans = math.ceil(save_amount * float(contractData['number']))
        param = {
            'amount': save_amount,  # 合同金额
            'totalBeans': totalBeans,  # 总迈豆
        }
        # log记录参数
        logParam = {
            'table': 'contract',
            'before': param,
            'after': param,
        }
        try:
            Model.objects.filter(id=id).update(**param)
            logParam.update(tableId=id)  # log记录参数
            logParam.update(action=6)  # log记录参数,action=2为修改

            logsform(request, logParam)
            return HttpResponse(json.dumps({'code': 200, 'msg': '操作成功!'}), content_type="application/json")
        except (ValueError, KeyError, TypeError):
            return HttpResponse(json.dumps({'code': 0,'msg':'json格式错误!'}), content_type="application/json")


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
            returnData = {'code':'200', 'msg': '操作成功!'}
        else:
            returnData = {'code': '0', 'msg': '操作失败!'}
    except Exception:
            returnData = {'code': '-1', 'msg': '非法请求!'}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

# 删除操作
@auth  # 引用登录权限验证
def delete(request):
    post = request.POST
    if post:
        selection = post.getlist('selection[]')
        try:
            model = Model.objects.filter(id__in=selection).delete()
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        if model:
            CreditRule.objects.filter(contractId__in=selection).delete()
            # 操作成功添加log操作记录
            for id in selection:
                # log记录参数
                logParam = {
                    'table': 'company',
                    'after': {},
                    'tableId': id,
                }
                logParam.update(action=5)  # log记录参数,action=5为删除
                logsform(request, logParam)
            returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
        else:
            returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
    else:
        returnData = {'code': '1000', 'msg': '不允许直接访问', 'data': None}
    return HttpResponse(json.dumps(returnData), content_type="application/json")

'''
前端访问接口
'''
@auth  # 引用登录权限验证
def contractlist(request, **kwargs):
    if request.method == 'POST':
        req = request.POST
        appId = req.get('appId')
    else:
        appId = kwargs.get('appId')
    returnFormat = kwargs.get('returnFormat')
    if appId:
        data = {}
        try:
            modelData = Model.objects.filter(status=1, appId=appId).order_by("id")
        except Exception:
            modelData = {}
        if modelData:
            for val in modelData:
                data[str(val.id)] = val.name
        if data:
            returnData = {'code': 200, 'msg': '操作成功', 'data': data}
        else:
            returnData = {'code': 200, 'msg': '暂无数据', 'data': None}
    else:
        returnData = {'code': 200, 'msg': '参数缺失', 'data': None}

    if returnFormat:
        return returnData.get('data')
    elif request.method == 'POST':
        return HttpResponse(json.dumps(returnData), content_type="application/json")
    else:
        return returnData.get('data')
