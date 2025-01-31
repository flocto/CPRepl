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
        self.left = None
        self.right = None
        self.height = height

class TrieNode(Node):
    def __init__(self, data, cnt = 0):
        super().__init__(data)
        self.children = {}
        self.cnt = cnt

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
#     print(f"Case #{I+1}: ", end="")
#     # Your code here
