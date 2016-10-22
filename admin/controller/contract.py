# coding:utf-8
# 管理员管理
__author__ = 'lxhui'
from admin.controller.common_import import *  # 公共引入文件
from admin.model.Contract import Contract as Model
from admin.model.Company import Company
from admin.model.CreditConfig import CreditConfig
from admin.model.CreditLog import CreditLog

@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    cid = post.get('cid','')
    name = post.get('name','').strip()
    code = post.get('code','').strip()
    data = Model.objects.filter(cid__icontains=cid,name__icontains=name,code__icontains=code).order_by('id')

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)

    '''企业信息'''
    comList = Company.objects.filter(status=1).order_by("id")

    return render(request, 'admin/contract/index.html',{
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
        'comList': comList,
    })


'''
保存合同信息
'''
@auth # 引用登录权限验证
def save(request, **param):
    post = request.POST
    if request.method == 'POST':
        param = {
            'id': post.get('id'),  # objectid
            'cid': post.get('cid'),  # 企业id
            'appId': post.get('appId'),  # 企业id
            'name':post.get('name'), # 合同名
            'code': post.get('code'),  # 合同编号
            'amount': post.get('amount'),# 合同金额
            'number': post.get('number'),  # 合同比例
            'img': post.get('img'),# 合同照片
            'startTime': post.get('startTime'),# 合同有效期
            'endTime': post.get('endTime'),# 合同截止日期
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

# 迈豆分配
@auth  # 引用登录权限验证
def credit(request):
    post = request.POST
    id = post.get('id')
    post_credit = int(post.get('credit1'))
    if id:
        try:
            contractGet = Model.objects.get(id=id)
            credit_poor = contractGet['number'] * contractGet['amount'] - contractGet['credit1']
        except Exception:
            returnData = {'code': '910', 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        # return HttpResponse(credit_poor)
        if credit_poor > post_credit:
            try:
                modelCreditConfig = CreditConfig.objects.get(contractId=id)
            except Exception:
                returnData = {'code': '912', 'msg': '找不到对应的应用平台信息', 'data': ''}
                return HttpResponse(json.dumps(returnData), content_type="application/json")
        else:
            returnData = {'code': '911', 'msg': '分配迈豆超出额度', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        extend_list = modelCreditConfig['extend']
        # 获取配置列表
        model_credit = modelCreditConfig['extend']['credit1']
        if model_credit:
            model_credit_int = int(model_credit)
        else:
            model_credit_int = 0
        if post_credit > 0:
            post_credit_int = post_credit
        else:
            post_credit_int = 0
        extend_list['credit1'] = model_credit_int + post_credit_int
        param = {
            'extend': extend_list,
        }
        contractCredit1 = int(contractGet['credit1']) + post_credit_int
        try:
            modelContract = Model.objects.get(id=contractGet['id']).update(credit1=contractCredit1)
            modelCreditConfigSave = CreditConfig.objects.get(id=modelCreditConfig['id']).update(**param)
            if modelCreditConfigSave == 1:
                returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
            else:
                returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
        except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}

        # 操作成功添加log操作记录
        if returnData.get('code') == '200':
            # log记录参数
            logParam = {
                'contractId': str(contractGet['id']),
                'credit1': post_credit_int,
            }
            try:
                CreditLog.objects.create(**logParam)
            except Exception:
                pass
    else:
        returnData = {'code': '1000', 'msg': '参数缺失', 'data': None}

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
