# coding=utf8
# Time    : 2020/4/25 11:42
# File    : sample.py
# Software: PyCharm

from src.func_utils.general import func_reg, DEFAULT_FUNC_INFO_DICT

d = {}


@func_reg(d)
def test():
    print("test")


if __name__ == '__main__':

    print(DEFAULT_FUNC_INFO_DICT.keys())
    for item in DEFAULT_FUNC_INFO_DICT.keys():
        print(item)
    print(d)
