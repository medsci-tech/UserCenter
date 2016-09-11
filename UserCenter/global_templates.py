#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 20160801
# @Author  : zhaiyu

def configParam(request):
    return {
        'c_adminInfo': {
            'username': 'zhaiyu',
        },
        'c_status': {
            0: '禁用',
            1: '启用',
        },
        'c_img_type': {
            'image/jpeg',
            'image/gif',
            'image/png',
        },
        'c_excel_type': {
            'application/vnd.ms-excel',
        },
        'c_page': 20,
        'c_cycle': {
            0: '不限',
            1: '一次',
            2: '每天',
            3: '整点',
            4: '间隔分钟',
        },
    }