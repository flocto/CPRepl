from math import *
from random import *
from collections import defaultdict, Counter
import itertools
import functools
import bisect
import sys
from sys import stdin, stdout
sys.setrecursionlimit(1_000_000_000)
MOD = 1_000_000_007

getnum = lambda: int(input())
getnums = lambda: map(int, input().split())
getlistnums = lambda: list(getnums())
getall = lambda: stdin.read()
getalllines = lambda: [x[:-1] for x in stdin.readlines()]

# T = getnum()
# for I in range(T):
#     print(f"Case #{I+1}: ", end="")
#     # Your code here

