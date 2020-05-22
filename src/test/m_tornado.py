# coding=utf8
# Time    : 2020/5/15 10:51
# File    : tornado.py
# Software: PyCharm
import functools
import tornado
from tornado import gen
from tornado.httpclient import AsyncHTTPClient


async def async_req(url):
    client = AsyncHTTPClient()
    resp = await client.fetch(url)
    return resp.body


urls = ["https://www.baidu.com", "https://www.sina.com"]

await_ables = map(lambda _: functools.partial(async_req, _), urls)

for item in await_ables:
    print(item)

# wait_iterator = gen.WaitIterator(await_ables)


# def item_wait():
#     while not wait_iterator.done():
#         try:
#             result = yield wait_iterator.next()
#         except Exception as e:
#             print(wait_iterator.current_index, e)
#         else:
#             print("Result {} received from {} at {}".format(
#                 result, wait_iterator.current_future,
#                 wait_iterator.current_index))
#

# item_wait()
