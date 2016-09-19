#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 20160801
# @Author  : zhaiyu

def configParam(request):
    return {
        # 状态
        'c_status': {
            0: '禁用',
            1: '启用',
        },

        # 图片上传格式
        'c_img_type': {
            'image/jpeg',
            'image/gif',
            'image/png',
        },

        # Excel表格上传格式
        'c_excel_type': {
            'application/vnd.ms-excel',
        },

        # 分页当前页显示条数
        'c_page': 20,

        # 积分策略周期
        'c_cycle': {
            0: '不限',
            1: '一次',
            2: '每天',
            3: '整点',
            4: '间隔分钟',
        },

        # 积分策略扩展
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

        # 系统记录操作
        'c_logs_operate': {
            0: '全部',
            -1: '删除',
            1: '添加',
            2: '修改',
        },
    }