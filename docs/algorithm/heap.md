# 大顶堆

这里过程不复杂。主要是上浮和下沉，30~40 行代码。上浮简单一些，下沉也不复杂
主要知识点有：
* 当前节点`n`, 父节点为 `(n-1) / 2` 子节点 分别为`2n+1` 、`2n+2`
* **插入元素**：插入到尾部，然后上浮，同时容量加一
* **弹出元素** ：首尾交换 然后下沉，同时容量减一， 并返回尾部元素

**上浮简单一些，下降要判断是否有子节点，以及 有可能子节点和当前节点 是在前一个状态下是同一个父节点**

注意：元素下沉的时候要判断是是否有左右节点 要注意隐含关系 **理想情况下，下降的时候 子节点一定大于父节点（原因是从最下面一层拿的值，在中间层是符合的），除非是前一个状态下有共同父节点**
* 当有左右节点的时候 此节点一定小于左右节点，只需比较左右节点就行,原因是从尾部来的元素
* 当没有右节点的时候 当前节点有可能是和左节点同一个父节点的 只有当前节点比左节点大的时候才继续 否则退出


```python
class Heap(object):

    def __init__(self, capacity):
        self.size = 0
        self.data = []
        self.capacity = capacity

    def put(self, ele):
        self.data.append(ele)
        self.size += 1
        self.float(self.size - 1)

    def pop(self):
        # 交换

        self.data[0], self.data[self.size - 1] = self.data[self.size - 1], self.data[0]
        self.size -= 1
        self.down()
        # print self
        return self.data[self.size]

    def float(self, n):
        parent = int((n - 1) / 2)
        if parent < 0:  # 只有一个元素
            return
        while parent >= 0:
            if self.data[n] > self.data[parent]:
                self.data[parent], self.data[n] = self.data[n], self.data[parent]
                n = parent
                parent = int((n - 1) / 2)
            else:
                break

    def down(self):
        n = 0
        l = 2 * n + 1
        r = 2 * n + 2
        end = self.size - 1
        while l <= end or r <= end:
            lv = self.data[l]
            # 有右节点
            if r <= end:
                rv = self.data[r]
                if lv > rv:
                    self.data[n], self.data[l] = self.data[l], self.data[n]
                    n = l
                else:
                    self.data[n], self.data[r] = self.data[r], self.data[n]
                    n = r
            else:
                # 没右节点
                # 可以向下
                if lv > self.data[n]:
                    self.data[n], self.data[l] = self.data[l], self.data[n]
                    n = l
                # 到达合适状态
                else:
                    break

            l = 2 * n + 1
            r = 2 * n + 2

    def __str__(self):
        return ", ".join([str(item) for item in self.data])


h = Heap(100)
for i in range(0, 16):
    h.put(i)
print("插入后的数组的值：", h)

print("依次弹出的：", [h.pop() for i in range(0, 15)])

print("弹出后的数组的值：", h)

```
