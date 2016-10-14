# -*- coding: utf-8 -*-
# 函数
# zhaiyu
from random import sample
import string

# 生成随机字符串
def random_str(length=8):
    char = string.ascii_letters + string.digits
    char_length = len(char)
    return ''.join([char[x] for x in sample(range(0, char_length), length)])
