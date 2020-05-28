# coding=utf8
# Time    : 2020/5/28 16:01
# File    : tornado.py
# Software: PyCharm
"""
基于tornado的IOLoop的定时器，用于任务的调度
也可以称为调度器

这里主要是使用tornado的循环用来实现定时器。
其中使用了超时，回调等内容。

这里是最小定时器，只有一个定时的,

可以结合令牌的处理限速的操作
当然也可以扩展为一个调度系统。
主要有 任务注册，任务发布。
    这时要提供一个任务注册中心，用于注册任务，提供任务列表
    任务中心之下根据不同的功能分成不同的区。
    任务的初始化 和任务的更新。通过添加timeout 定时更新任务列表。
    如果遇到任务没提交，直接进行任务更新。 如果任务多次更新超过一定次数之后,仍然没发现配置, 就直接投放垃圾队列

    同时要提供任务存储地方，这里可以是mongo,等其他存储
    根据大的功能区分到不同的位置，以下次运行距离时间大小排序  类似于celery的eta队列，只不过这是分布式的。

    任务的发布：
    主要提交一些异步任务

同时根据需要可以提供一个心跳接口，用于向调度中心标明接口存活，可以使用timeout 实现。
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
