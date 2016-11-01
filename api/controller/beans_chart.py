# -*- coding: utf-8 -*-

from api.controller.common_import import *  # 公共引入文件

from admin.model.BeanLog import BeanLog
# 时间模块
import datetime
import math
'''
    积分图表接口
'''


# ============================
# 用户积分操作api
# ============================
@csrf_exempt
def list(request):
    post = request.POST
    if not post:
        return ApiResponse(200,'hehe').json_response()



# ============================
# 用户积分log记录添加--private
# ============================
