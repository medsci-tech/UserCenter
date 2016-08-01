#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 20160801
# @Author  : zhaiyu

def userInfo(request):
    info = {
        'username' : 'zhaiyu',
    }
    return {'userInfo': info}