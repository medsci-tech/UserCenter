#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 20160801
# @Author  : zhaiyu

def configParam(request=None):
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
            3: '每月',
        },

        # 积分策略扩展
        # 'c_ext_credit': {
        #     'credit1': '迈豆',  # 迈豆为第一个扩展
        # },

        # 系统记录操作
        'c_logs_operate': {
            1: '添加',
            2: '修改',
            3: '启用',
            4: '禁用',
            5: '删除',
            6: '充值',
        },

        # 用户角色 doctor->医生, user->患者,volunteer->代表，agency->代理商 ,company->企业
        'c_user_role': {
            'doctor': '医生',
            'user': '患者',
            'volunteer': '代表',
            'agency': '代理商',
            'company': '企业',
            'enterprise': '运营',
        },

        # 安全令牌
        'c_token': {
            'key': '123abc',  # token密钥
            'expire': None,  # 有效期
        },

        # app_id 对应数据库objectId
        'c_api_appId': {
            1: '58183aab4eaa76339b2ee36b',  # 药械通微信端
            2: '58183acb4eaa7633bc2ee36b',  # 易康伴侣微信端
        }
    }