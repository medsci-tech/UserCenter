# coding:utf-8
# 管理员管理
# zhaiyu
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from UserCenter.global_templates import configParam
from UserCenter.settings import UPLOAD_ROOT, UPLOAD_URL
from datetime import *
import time
import os
import json
import random
import re

# 文件上传.
def handle_uploaded_file (filepath, file):
    time_now = datetime.now()
    pattern = re.compile(r'.[A-Za-z]*$')
    suffix = pattern.findall(file.name)
    save_path = '%s/%s' % (filepath, time_now.strftime('%Y%m'))
    save_name = '%s%s%s' % (time.time(), random.randint(1000, 9999), str(suffix[0]))
    path = '%s/%s/' % (UPLOAD_ROOT, save_path)
    if not os.path.exists(path):
        os.makedirs(path)
    f = path + save_name
    fd = open(f, 'wb+')
    try:
        for chunk in file.chunks():
            fd.write(chunk)
        returnData = {'code': '200', 'msg': '成功', 'data': '%s%s/%s' % (UPLOAD_URL, save_path, save_name)}
    except Exception:
        returnData = {'code': '900', 'msg': '失败', 'data': ''}
    finally:
        fd.close()
    return returnData

# 上传图片
@csrf_exempt
def img(request):
    cfg_param = configParam(request)
    file = request.FILES.get('file')
    file_path = request.GET.get('path')
    file_type = cfg_param.get('c_img_type')
    if file.content_type in file_type:
        try:
            save_name = handle_uploaded_file(file_path, file)
            if save_name.get('code') == '200':
                returnData = {'code': '200', 'msg': '成功', 'data': {'tName': file.name, 'saveName': [save_name.get('data')]}}
            else:
                returnData = {'code': '802', 'msg': '失败', 'data': ''}
        except Exception:
            returnData = {'code': '900', 'msg': '失败', 'data': ''}
    else:
        returnData = {'code': '801', 'msg': '文件格式不支持', 'data': ''}

    return HttpResponse(json.dumps(returnData), content_type="application/json")
