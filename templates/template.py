from math import *
from random import *
from heapq import *
from bisect import *
from collections import defaultdict, Counter, deque
from fractions import Fraction
import itertools
import functools
import os
import sys
from graphlib import TopologicalSorter, CycleError
sys.setrecursionlimit(10**7)
from sys import stdin, stdout
MOD = 10**9 + 7

BUFSIZE = 8192
from io import BytesIO, IOBase
class FastIn(IOBase):
    def __init__(self, file):
        self._fd = file.fileno()
        self._buffer = BytesIO()
        self.lines = 0
    
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self._buffer.tell()
            self._buffer.seek(0, 2), self._buffer.write(b), self._buffer.seek(ptr)
        self.lines = 0
        return self._buffer.read()

    def readline(self):
        while self.lines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.lines = b.count(b"\n") + (not b)
            ptr = self._buffer.tell()
            self._buffer.seek(0, 2), self._buffer.write(b), self._buffer.seek(ptr)
        self.lines -= 1
        return self._buffer.readline()
    
class FastOut(IOBase):
    def __init__(self, file):
        self._fd = file.fileno()
        self._buffer = BytesIO()
    
    def write(self, s):
        if isinstance(s, str):
            s = s.encode()
        self._buffer.write(s)
    
    def flush(self):
        os.write(self._fd, self._buffer.getvalue())
        self._buffer.truncate(0), self._buffer.seek(0)

class Node:
    def __init__(self, data):
        self.data = data

class ListNode(Node):
    def __init__(self, data, next = None):
        super().__init__(data)
        self.next = next

class TreeNode(Node):
    def __init__(self, data, left = None, right = None, height = 0):
        super().__init__(data)
        self.left = left
        self.right = right
        self.height = height

class TrieNode(Node):
    def __init__(self, data, cnt = 0, height = 0):
        super().__init__(data)
        self.children = {}
        self.cnt = cnt
        self.height = height

class PriorityQueue:
    # min pq by default
    def __init__(self, arr = None, key = lambda x: x):
        self.key = key
        self.arr = arr if arr else []
        heapify(self.arr)
    
    def push(self, x):
        heappush(self.arr, x)
    
    def pop(self):
        return heappop(self.arr)
    
    def top(self):
        return self.arr[0]

    def __len__(self):
        return len(self.arr)

    def __bool__(self):
        return bool(self.arr)
    
    def __repr__(self):
        return f"PriorityQueue({self.arr})"
    
    def __str__(self):
        return repr(self)

    def __iter__(self):
        return iter(self.arr)

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.height = [0] * n
        self.size = [1] * n
        self.num_sets = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        self._union_by_height(x, y)
        # self._union_by_size(x, y)

    def _union_by_size(self, x, y):
        x, y = self.find(x), self.find(y)
        if x != y:
            if self.size[x] < self.size[y]:
                x, y = y, x
            self.parent[y] = x
            self.size[x] += self.size[y]
            self.num_sets -= 1
    
    def _union_by_height(self, x, y):
        x, y = self.find(x), self.find(y)
        if x != y:
            if self.height[x] < self.height[y]:
                x, y = y, x
            self.parent[y] = x
            if self.height[x] == self.height[y]:
                self.height[x] += 1
            self.num_sets -= 1

    def set_size(self, x):
        return self.size[self.find(x)]

    def __len__(self):
        return self.num_sets

    def __repr__(self):
        return f"UnionFind({self.num_sets})"

    def __str__(self):
        return repr(self)

# LOL what the hack is this 
def topsort(graph):
    try:
        ts = TopologicalSorter(graph)
        return list(ts.static_order())
    except CycleError:
        return False # cycle found
    
def edges2graph(edges, directed=False):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph

def find_le(arr, x):
    i = bisect_right(arr, x)
    if i:
        return i-1, arr[i-1]
    return -1, None

def find_ge(arr, x):
    i = bisect_left(arr, x)
    if i != len(arr):
        return i, arr[i]
    return -1, None

input = FastIn(stdin).readline
stdout = FastOut(stdout)
exit = sys.exit

INF = float("inf") 

def print(*args, **kwargs):
    end = kwargs.get("end", "\n")
    sep = kwargs.get("sep", " ")
    stdout.write(sep.join(map(str, args)) + end)

getnum = lambda: int(input())
getnums = lambda: map(int, input().split())
getwords = lambda: input().split()
getlistnums = lambda: list(getnums())
getall = lambda: stdin.read()
getalllines = lambda: [x.rstrip() for x in stdin.readlines()]

# T = getnum()
# for I in range(T):
#     # print(f"Case #{I+1}: ", end="")
#     # Your code here
