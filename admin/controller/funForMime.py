# coding:utf-8
# 函数
# zhaiyu
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
from UserCenter.global_templates import configParam

# 分页
def paginationForMime(**kwargs):
    data = kwargs.get('data')
    pageStart = int(kwargs.get('page'))  # 获取页码

    cfg_param = configParam()
    limit = cfg_param.get('c_page')  # 每页显示的记录数

    try:
        pageSizeLength = int(kwargs.get('length'))  # 当前n页页码
    except Exception as e:
        pageSizeLength = 7  # 默认中间页数

    paginator = Paginator(data, limit)  # 实例化一个分页对象
    try:
        data_list = paginator.page(pageStart)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        data_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        data_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    GetListPageCount = int(paginator.num_pages)  # 总页数
    page_pre = pageStart - math.floor(pageSizeLength / 2)
    page_next = pageStart + math.ceil(pageSizeLength / 2)
    assign_pageLengthNext = 0
    assign_pageLengthPrev = 0
    if (GetListPageCount > pageSizeLength):
        # 总条数大于中间n页
        assign_pageStart = page_pre if page_pre > 1 else 1
        assign_pageEnd = page_next if page_next < (GetListPageCount + 1) else (GetListPageCount + 1)
        if page_pre > 1:
            assign_pageLengthPrev = (pageStart - pageSizeLength) if pageStart - pageSizeLength > 1 else 1
        if page_next < GetListPageCount + 1:
            assign_pageLengthNext = (pageStart + pageSizeLength) if pageStart + pageSizeLength < GetListPageCount else GetListPageCount
        if page_pre <= 1:
            assign_pageEnd = pageSizeLength + 1
        if page_next >= GetListPageCount + 1:
            assign_pageStart = GetListPageCount + 1 - pageSizeLength
    else:
        assign_pageStart = 1
        assign_pageEnd = GetListPageCount + 1

    return {
        'data_list' : data_list,
        'pageLengthPrev' : assign_pageLengthPrev,
        'pageLengthNext' : assign_pageLengthNext,
        'pageStart' : assign_pageStart,
        'pageLast' : GetListPageCount,
        'pageEnd' : assign_pageEnd,
    }