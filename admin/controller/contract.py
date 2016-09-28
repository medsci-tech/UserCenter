# coding:utf-8
# 管理员管理
__author__ = 'lxhui'
from admin.controller.common_import import * # 公共引入文件
from admin.model.Contract import Contract
from admin.model.Company import Company
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
    return render(request, 'admin/contract/index.html',{'list':list, 'post': post, 'comList': comList})


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
    try:
        model = Contract.objects.filter(pk__in=selection).delete() # 删除
        #model = Contract.objects.filter(pk__in=selection).update(**param)
        if model:
            returnData = {'code':'200', 'msg': '操作成功!'}
        else:
            returnData = {'code': '0', 'msg': '操作失败!'}
    except Exception:
            returnData = {'code': '-1', 'msg': '非法请求!'}

    return HttpResponse(json.dumps(returnData), content_type="application/json")