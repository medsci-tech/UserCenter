# coding:utf-8
# 管理员管理
# zhaiyu
from django.shortcuts import render
from users.model.Contract import Contract
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


# 上传图片
@csrf_exempt
def img(request):
    post = request.POST
    file = request.FILES.get('file')
    # try:
    #     model = Contract(**param).editByIds(selection, **param)
    #     if model.get('n'):
    #         if model.get('ok'):
    #             returnData = {'code': '200', 'msg': '操作成功', 'data': ''}
    #         else:
    #             returnData = {'code': '801', 'msg': '操作失败', 'data': ''}
    #     else:
    #         returnData = {'code': '802', 'msg': '不存在的数据集', 'data': ''}
    # except Exception:
    returnData = {'code': '900', 'msg': '数据验证错误', 'data': post}

    # return HttpResponse(post.get('type'))
    return HttpResponse(json.dumps(returnData), content_type="application/json")
