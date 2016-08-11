# coding:utf-8
# 函数
# zhaiyu
from django.core.paginator import Paginator
import math

# 分页函数
class JuncheePaginator(Paginator):
    def __init__(self, object_list, per_page, range_num=5, orphans=0, allow_empty_first_page=True):
        Paginator.__init__(self, object_list, per_page, orphans, allow_empty_first_page)
        self.range_num = range_num

    def page(self, number):
        self.page_num = number
        return super(JuncheePaginator, self).page(number)

    def _page_range_ext(self):
        num_count = 2 * self.range_num + 1
        if self.num_pages <= num_count:
            return range(1, self.num_pages + 1)
        num_list = []
        num_list.append(self.page_num)
        for i in range(1, self.range_num + 1):
            if self.page_num - i <= 0:
                num_list.append(num_count + self.page_num - i)
            else:
                num_list.append(self.page_num - i)

            if self.page_num + i <= self.num_pages:
                num_list.append(self.page_num + i)
            else:
                num_list.append(self.page_num + i - num_count)
        num_list.sort()
        return num_list

    page_range_ext = property(_page_range_ext)

def page(**kwargs):
    pageStart = int(kwargs.get('page'))  # 当前页码
    GetListCount = int(kwargs.get('count'))  # 总条数
    try:
        pageSizeLength = int(kwargs.get('length'))  # 当前n页页码
        size = kwargs.get('size')   # 当前页显示条数
    except Exception as e:
        pageSizeLength = 7  # 默认中间页数
        size = 20  # 默认当前页显示条数
    GetListPageCount = int(GetListCount) / int(size)  # 总页数
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
        'pageLengthPrev' : assign_pageLengthPrev,
        'pageLengthNext' : assign_pageLengthNext,
        'pageStart' : assign_pageStart,
        'pageEnd' : assign_pageEnd,
    }