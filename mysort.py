from timeit import timeit
from random import randrange
import sys
#sys.setrecursionlimit(10**9)
def selection_sort(arr):
    """
    >>> selection_sort([3, 1, 4])
    [1, 3, 4]
    """
    a=arr.copy()
    for i in range(len(a)):
        min_idx=i
        for j in range(i+1,len(a)):
            if a[min_idx]>a[j]:
                min_idx=j
        a[i],a[min_idx]=a[min_idx],a[i]
    return a

def quick_sort(arr):
    """
    >>> quick_sort([3, 1, 4])
    [1, 3, 4]
    """
    a=arr.copy()
    if len(a)<=1:
        return a
    pivot = a[0]
    left  = [x for x in a if x < pivot]
    mid   = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]

    return quick_sort(left)+mid+quick_sort(right)

def benchmark(n: int = 10000, repeat: int = 3) -> None:
    """1 万件ランダム整数で平均実行時間を出力"""
    setup = (
        "from __main__ import selection_sort, quick_sort, randrange;"
        f"data=[randrange({n}) for _ in range({n})]"
    )
    sel = timeit("selection_sort(data)", setup=setup, number=repeat) / repeat
    qck = timeit("quick_sort(data)", setup=setup, number=repeat) / repeat
    print(f"{n=}, {repeat=}")
    print(f"selection_sort: {sel:.3f}s   quick_sort: {qck:.3f}s")
    
if __name__ == "__main__":
    print(selection_sort([3, 1, 4]))
    print(quick_sort([3, 1, 4]))
    benchmark()



