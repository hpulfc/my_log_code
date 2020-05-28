# coding=utf8
# Time    : 2020/5/28 16:01
# File    : tornado.py
# Software: PyCharm
"""
基于tornado的IOLoop的定时器

这里主要是使用tornado的循环用来实现定时器。
其中使用了超时，回调等内容。

这里是最小定时器， 也及时只有一个定时的
"""
import datetime
from datetime import timedelta
from functools import wraps
from tornado.ioloop import IOLoop
from src.func_utils.timer import BaseTimer


def run_in_loop(func):
    """使提交任务操作位于loop中执行"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._io_loop.add_callback(func, self, *args, **kwargs)

    return wrapper


class TornadoTimer(BaseTimer):
    _io_loop = None
    _timeout = None

    def __init__(self):
        super(TornadoTimer, self).__init__()

    def _configure(self, config):
        self._io_loop = IOLoop.current()
        super()._configure(config)

    def _start_timer(self, wait_seconds, *args, **kwargs):
        self._stop_timer(*args, **kwargs)
        if wait_seconds:
            self._timeout = self._io_loop.add_timeout(timedelta(seconds=wait_seconds), self.wake_up, *args, **kwargs)

    def _stop_timer(self, *args, **kwargs):
        """移除定时器"""
        if self._timeout:
            self._io_loop.remove_timeout(self._timeout)
            del self._timeout

    @run_in_loop
    def wake_up(self, *args, **kwargs):
        self._stop_timer(*args, **kwargs)
        wait_seconds = self._worker(*args, **kwargs)
        self._start_timer(wait_seconds, *args, **kwargs)

    def _worker(self, *args, **kwargs):
        """要提交的执行的定时任务 在这里进行提交"""
        print("---------- begin worker ----------")
        print(datetime.datetime.now())
        print("---------- end worker ------------")
        return 3


if __name__ == '__main__':
    TornadoTimer().start()
    IOLoop.current().start()
