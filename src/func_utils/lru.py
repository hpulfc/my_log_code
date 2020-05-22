# coding=utf8
# Time    : 2020/4/28 11:40
# File    : lru.py
# Software: PyCharm


class Node(object):
    def __init__(self, val, l, r, k):
        self.parent = l
        self._next = r
        self.val = val
        self.k = k


class NodeList(object):
    """双向链表"""

    def __init__(self):
        self.tail = None
        self.head = Node("", None, None, "")

    def del_item(self, node):
        """
        从链表中删除对应的node
        :param node: Node 类型
        :return:
        """
        parent = node.parent
        _next = node._next
        parent._next = _next
        if _next:
            _next.parent = parent

        # 最后一个元素
        if node._next == None:
            self.tail = parent
            # print self.tail.val

        node._next = None
        node.parent = None
        return node

    def insert_head(self, node):
        """
        在头部添加
        :param item: 插入到头部
        :return:
        """
        # 更新tail
        if self.head._next == None:
            self.tail = node

        _tmp = self.head._next
        if _tmp:
            _tmp.parent = node
        node._next = _tmp
        node.parent = self.head
        self.head._next = node
        return node

    def del_tail(self):
        tail = self.del_item(self.tail)
        return tail

    def __str__(self):
        r = []
        _head = self.head._next
        while _head:
            r.append(str(_head.val))
            _head = _head._next
        return ", ".join(r)


class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.size = 0
        self.data = {}
        self.nl = NodeList()

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        # print self.nl
        node = self.data.get(key)
        if node:
            node = self.nl.del_item(node)
            self.nl.insert_head(node)
            return node.val
        else:
            return -1

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        # node = self.data.get(key)
        # if node:
        #     node = self.nl.del_item(node)
        #     self.size -= 1

        # if self.get(key) != -1:
        #     self.nl.del_head()
        node = self.data.get(key)

        if node:
            self.nl.del_item(node)
            self.size -= 1
            self.data.pop(key)

        node = self.nl.insert_head(Node(value, None, None, key))
        self.data[key] = node
        self.size += 1
        if self.size > self.capacity:
            tail = self.nl.del_tail()
            self.data.pop(tail.k)
            self.size -= 1

        # print self.nl

lru = LRUCache(3)
lru.put("a", 1)
lru.put("b", 2)
lru.put("c", 3)
lru.put("d", 4)
lru.get("a")