# coding=utf8
# Time    : 2020/4/25 11:32
# File    : general.py
# Software: PyCharm
import weakref
from functools import wraps


def hello():
    print("hello is not greet!")


DEFAULT_FUNC_INFO_DICT = weakref.WeakValueDictionary()


def func_reg(info_dict=None):
    """
    就是一个简简单单朴实无华的函数装饰器， 函数名和函数地址映射起来

    价值所在，不用手动的使用写死对应关系
    :param info_dict: 可以为空， 可以自己传入
    :return:
    """

    info_dict = DEFAULT_FUNC_INFO_DICT if info_dict is None else info_dict

    def _func_reg(func):
        func_template = "{}#{}"

        def _add_info_dict(_name):
            info_dict[_name] = func

        _add_info_dict(
            func_template.format(func.__module__, func.__name__)
        )

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result

        return wrapper

    return _func_reg
