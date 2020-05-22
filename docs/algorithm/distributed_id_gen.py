# coding=utf8
# Time    : 2020/5/22 18:11
# File    : distributed_id_gen.py
# Software: PyCharm
"""
线程安全的分布式ID生成器

"""
import os
import time
import random
import binascii
import socket
import hashlib
import threading
import struct
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

_m_hash = hashlib.md5()
_m_hash.update(socket.gethostname().encode())
machine_bytes = _m_hash.hexdigest()[:3]


class IDGen(object):
    """时间+机器+进程+自增数"""

    generate_lock = threading.RLock()
    max_incr = 0xFFFFFF
    max_pid = 0xFFFF
    incr = random.randint(0, max_incr)

    host_name = socket.gethostname()
    machine_bytes = machine_bytes
    pid = os.getpid() % max_pid

    fmt = binascii.hexlify

    @classmethod
    def id(cls):
        with IDGen.generate_lock:
            # 4 字节
            current_time = struct.pack(">i", int(time.time()))
            # 3 字节
            _machine = machine_bytes[:3].encode()

            # 2 字节
            _pid = struct.pack(">H", cls.pid)

            # 3 字节
            _incr = struct.pack(">i", cls.incr)[1:4]
            # print(type(_machine))
            _id = current_time + _machine + _pid + _incr

            cls.incr = (cls.incr + 1) % cls.max_incr
            return binascii.hexlify(_id)


def g_id():
    return IDGen.id()


def w():
    with ThreadPoolExecutor(max_workers=8) as executor:
        task = [executor.submit(g_id) for _ in range(0, 10 ** 4)]
        result = [r.result() for r in as_completed(task)]
        result = sorted(result)
        print(result)


if __name__ == '__main__':
    w()
