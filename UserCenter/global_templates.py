#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-10-31 14:26:26
# @Author  : Weizhong Tu (mail@tuweizhong.com)

def userInfo(request):
    info = {
        'username' : 'zhaiyu',
    }
    return {'userInfo': info}