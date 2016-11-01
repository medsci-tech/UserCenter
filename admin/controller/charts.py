# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# 扩展基础管理

# 公共引入文件
from admin.controller.common_import import *


def index(request):
    return render(request, 'admin/charts/index.html')