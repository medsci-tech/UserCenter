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
        'c_ext_credit': {
            'credit1': '扩展1',
            'credit2': '扩展2',
            'credit3': '扩展3',
            'credit4': '扩展4',
            'credit5': '扩展5',
            'credit6': '扩展6',
            'credit7': '扩展7',
            'credit8': '扩展8',
        },
    }