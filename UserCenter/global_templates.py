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
            '0': '禁用',
            '1': '启用',
        },
        'c_img_type':{
            'image/jpeg',
            'image/gif',
            'image/png',
        },
        'c_excel_type':{
            'application/vnd.ms-excel',
        },
    }