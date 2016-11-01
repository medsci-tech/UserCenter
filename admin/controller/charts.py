# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *


@csrf_exempt
@auth # 引用登录权限验证
def index(request):
    return render(request, 'admin/charts/index.html')