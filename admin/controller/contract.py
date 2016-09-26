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
    cid = post.get('cid',0)
    name = post.get('name','').strip()
    code = post.get('code','').strip()
    data = Contract.objects.filter(name__icontains=name,code__icontains=code).order_by('id')
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
        try:
            if(not id): # 添加操作
                Contract.objects.create(**param)
            else: # 更新
                Contract.objects.filter(id=id).update(**param)

            return HttpResponse(json.dumps({'code': 200, 'msg': '操作成功!'}), content_type="application/json")
        except (ValueError, KeyError, TypeError):
            return HttpResponse(json.dumps({'code': 0,'msg':'json格式错误!'}), content_type="application/json")

# 更改状态操作
@csrf_exempt
@auth # 引用登录权限验证
def stats(request):
    post = request.POST
    selection = post.getlist('selection[]')
    statusType = post.get('statusType')
    if statusType == 'enable':
        status = '1'
    else:
        status = '0'
    param = {
        'status': status,
    }

    try:
        model = Contract(**param).editByIds(selection, **param)
        if model.get('n'):
            if model.get('ok'):
                returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
            else:
                returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
        else:
            returnData = {'code': '802', 'msg': '不存在的数据集', 'data': ''}
    except Exception:
            returnData = {'code': '900', 'msg': '数据验证错误', 'data': ''}

    return HttpResponse(json.dumps(returnData), content_type="application/json")

def test(request):
    return render(request, 'admin/common/test.html')