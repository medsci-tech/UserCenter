#_*_coding:utf-8_*_
# 管理员管理
__author__ = 'lxhui'
from admin.controller.common_import import * # 公共引入文件
from admin.model.Admin import Admin
from django.contrib.auth.hashers import make_password,check_password
'''
管理员列表
'''
@csrf_exempt
@auth # 引用登录权限验证
def list(request):
    post = request.POST
    username = post.get('username','').strip()
    nickname = post.get('nickname','').strip()
    email = post.get('email','').strip()
    data = Admin.objects.filter(username__icontains=username,email__icontains=email,nickname__icontains=nickname).order_by('id')

    page = request.GET.get('page', 1)  # 获取页码
    pageData = paginationForMime(page=page, data=data)

    return render(request, 'admin/admin/index.html',{
        'data_list': pageData.get('data_list'),
        'page_has_previous': pageData.get('pageLengthPrev'),
        'page_has_next': pageData.get('pageLengthNext'),
        'page_last': pageData.get('pageLast'),
        'page_range': range(pageData.get('pageStart'), pageData.get('pageEnd')),
        'ctrlList': post,
    })

'''
保存管理员
'''
@auth # 引用登录权限验证
def save(request, **param):
    post = request.POST
    if request.method == 'POST':
        model = Admin()
        param = {
            'id': post.get('id'),  # objectid
            'username':post.get('username'), # 用户名
            'password': make_password(post.get('pwd', '123456'), None, 'pbkdf2_sha256'), # 加密,
            'nickname':post.get('nickname', None),  # 昵称
            'email': post.get('email'),  # 邮箱
            'status': post.get('status')  # 状态
        }
        id = param.get('id',0)
        param.pop('id') # 剔除主键

        try:
            if(not id): # 添加操作
                json_str = model.checkUsername(username=param.get('username', None))
                decoded = json.loads(json_str)
                if(not decoded['status']): # 如果用户存在
                    return HttpResponse(json_str)
                else:
                    Admin.objects.create(**param)
                    return HttpResponse(json_str)
            else: # 更新
                if(not post.get('pwd')): # 密码为空则不修改密码
                    param.pop('password')

                '''处理用户是否存在'''
                res = Admin.objects.get(id=id)
                if res.username != param.get('username', None):
                    json_str = model.checkUsername(username=param.get('username', None))
                    decoded = json.loads(json_str)
                    if (not decoded['status']):  # 如果用户存在
                        return HttpResponse(json_str)
                    
                Admin.objects.filter(id=id).update(**param)
                return HttpResponse(json.dumps({'status': 1, 'msg': '修改成功!'}))
        except (ValueError, KeyError, TypeError):
            return HttpResponse(json.dumps({'status': 0,'msg':'json格式错误!'}))


def detail(request, question_id):
    pass
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    # return render(request, 'admin/admin/detail.html', {'question': question})

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
        model = Admin.objects.filter(pk__in=selection).update(**param)
        if model:
            returnData = {'status':1, 'msg': '操作成功!'}
        else:
            returnData = {'status': '0', 'msg': '操作失败!'}
    except Exception:
            returnData = {'status': '0', 'msg': '非法请求!'}

    return HttpResponse(json.dumps(returnData))

