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
    }