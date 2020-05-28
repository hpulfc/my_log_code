# coding=utf8
# Time    : 2020/5/28 16:00
# File    : __init__.py.py
# Software: PyCharm
"""定时器的实现，Timer"""
import six
import abc


class BaseTimer(six.with_metaclass(abc.ABCMeta, object)):

    def __init__(self):
        self.configure()

    def configure(self, *args, **kwargs):
        # do somethings
        # do somethings

        config = kwargs
        self._configure(config)

    def _configure(self, config):
        pass

    def start(self, *args, **kwargs):
        print("start ...")
        self.wake_up(*args, **kwargs)

    @abc.abstractmethod
    def _worker(self, *args, **kwargs):
        """提交任务，并获取下一个任务 在几秒后执行"""
        raise NotImplementedError

    @abc.abstractmethod
    def wake_up(self, *args, **kwargs):
        raise NotImplementedError