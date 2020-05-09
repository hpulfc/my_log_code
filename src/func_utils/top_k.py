# coding=utf8
# Time    : 2020/5/9 19:05
# File    : top_k.py
# Software: PyCharm
"""
top k 算法的实现

使用小顶堆，先加载前k个元素，
然后遍历依次和堆顶元素比较，
如果元素大于堆顶元素，则弹出堆顶，推入当前元素
"""

import heapq


def top_k(target, k, push=heapq.heappush, pop=heapq.heappop):
    _m = []
    for i in range(0, k):
        push(_m, target[i])

    for i in range(k, len(target)):
        if _m[0] < target[i]:
            pop(_m)
            push(_m, target[i])
    return [pop(_m) for _ in range(k)]


import time

_s = time.time()
print(top_k(range(10 ** 8), 5))
print(time.time() - _s)

# [99999995, 99999996, 99999997, 99999998, 99999999]
# 55.59917998313904
# 一亿个数用时55 秒

