# coding=utf8
# Time    : 2020/4/25 14:07
# File    : rate_limit.py
# Software: PyCharm
"""
Token Budget for rate limit

就是简单的单线程令牌桶
可以根据需要扩展分布式的
"""

import time
import json


class TokenBudget(object):

    def __init__(self, recover_rate, capacity=1):
        self.capacity = capacity
        self._tokens = capacity
        self.rate = recover_rate
        self.timestamp = time.time()

    def consume(self, tokens=1):
        """
        消费掉令牌

        :param tokens:token 数量
        :return:
        """
        if self.tokens > tokens:
            self._tokens -= tokens
            return True
        return False

    def expect_time(self, token=1):
        """获取这么多的token需要多长时间"""
        _tokens = self.tokens()
        if token < _tokens:
            return 0
        else:
            return (token - _tokens) / self.rate

    @property
    def tokens(self):
        """获取token的数量，每次获取都要刷新token，同时更新时间戳"""
        if self._tokens < self.capacity:
            now = time.time()
            self._tokens = min(self.capacity, self._tokens + self.rate * (now - self.timestamp))
            self.timestamp = now
        return self.tokens


class SampleTokenBudget(TokenBudget):

    def __init__(self, recover_rate, capacity=1):
        super(SampleTokenBudget, self).__init__(recover_rate, capacity)

    def __str__(self):
        """为了序列化"""
        doc = {"capacity": self.capacity, "_tokens": self._tokens, "rate": self.rate, "timestamp": self.timestamp}
        return json.dumps(doc)

    def load_state(self, stat_str):
        body = json.load(stat_str)
        self.timestamp = body.get("timestamp")
        assert self.timestamp
        self.rate = body.get("rate")
        assert self.rate
        self._tokens = body.get("_tokens")
        assert self._tokens
        self.capacity = body.get("capacity")
        assert self.capacity

    @classmethod
    def load_instance(cls, instance_str):
        body = json.load(instance_str)
        capacity = body.get("capacity")
        rate = body.get("rate")
        return cls(rate, capacity)
