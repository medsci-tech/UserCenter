# coding:utf-8
# 管理员管理
__author__ = 'lxhui'
from admin.controller.common_import import *  # 公共引入文件
from admin.model.Contract import Contract
from admin.model.Company import Company
from admin.model.App import App
from admin.model.CreditConfig import CreditConfig
from admin.model.CreditLog import CreditLog

@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    post = request.POST
    cid = post.get('cid','')
    name = post.get('name','').strip()
    code = post.get('code','').strip()
    data = Contract.objects.filter(cid__icontains=cid,name__icontains=name,code__icontains=code).order_by('id')
    limit = 20  # 每页显示的记录数
    paginator = Paginator(data, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        list = paginator.page(paginator.num_pages)

    '''企业信息'''
    comList = Company.objects.filter(status=1).order_by("id")
    appList = App.objects.filter(status=1).order_by("id")
    return render(request, 'admin/contract/index.html',{'list':list, 'post': post, 'comList': comList, 'appList': appList})


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
                obj = Contract.objects.create(**param)
                logParam.update(tableId=obj.id)  # log记录参数
                logParam.update(action=1)  # log记录参数,action=1为添加
            else: # 更新
                Contract.objects.filter(id=id).update(**param)
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
        #model = Contract.objects.filter(pk__in=selection).delete() # 删除
        model = Contract.objects.filter(pk__in=selection).update(**param)
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
    companyId = post.get('companyId')
    appId = post.get('appId')
    post_credit = int(post.get('credit1'))
    if id and companyId and appId:
        try:
            contractGet = Contract.objects.get(id=id)
            credit_poor = contractGet['number'] * contractGet['amount'] - contractGet['credit1']
        except Exception:
            returnData = {'code': '910', 'msg': '数据验证错误', 'data': ''}
            return HttpResponse(json.dumps(returnData), content_type="application/json")
        # return HttpResponse(credit_poor)
        if credit_poor > post_credit:
            try:
                modelCreditConfig = CreditConfig.objects.get(companyId=companyId, appId=appId)
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
            modelContract = Contract.objects.get(id=contractGet['id']).update(credit1=contractCredit1)
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
                'appId': appId,
                'credit1': post_credit_int,
            }
            try:
                CreditLog.objects.create(**logParam)
            except Exception:
                pass
    else:
        returnData = {'code': '1000', 'msg': '参数缺失', 'data': None}

    return HttpResponse(json.dumps(returnData), content_type="application/json")