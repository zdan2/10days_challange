from __future__ import annotations
from typing import Iterable

class cached_property_custom:

    def __init__(self, func):
        self.func = func
        self.func_name = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # インスタンスの__dict__に値をキャッシュすることで、
        # 次回以降のアクセスではこの__get__を通さずに直接値が返される。
        value = self.func(instance)
        instance.__dict__[self.func_name] = value
        return value


class NumberStats:
    """統計値計算ユーティリティ

    >>> ns = NumberStats(10, 8, 3, 3, 8)
    >>> ns.size
    5
    >>> ns.mean
    6.4
    >>> ns.median
    8
    >>> ns.mode
    [3, 8]
    >>> round(ns.variance, 2)
    9.3
    
    # 偶数個のデータで中央値が正しく計算されることを確認
    >>> ns_even = NumberStats(1, 5, 2, 8)
    >>> ns_even.median
    3.5
    """

    def __init__(self, *values: float | int):
        if not values:
            raise ValueError("at least one number is required")
        self._values: tuple[float | int, ...] = tuple(values)

    # -------- cached properties --------
    @cached_property_custom
    def size(self) -> int:
        """データ数を返します。"""
        return len(self._values)

    @cached_property_custom
    def mean(self) -> float:
        """平均値を返します。"""
        return sum(self._values) / self.size

    @cached_property_custom
    def _sorted(self) -> tuple[float | int, ...]:
        """ソート済みのデータタプルを返します（内部利用）。"""
        # sorted() は組み込み関数
        return tuple(sorted(self._values))

    @cached_property_custom
    def median(self) -> float | int:
        """中央値を返します。"""
        n = self.size
        center_index = n // 2
        if n % 2 == 1:
            # データ数が奇数の場合
            return self._sorted[center_index]
        else:
            # データ数が偶数の場合、中央の2つの値の平均
            return (self._sorted[center_index - 1] + self._sorted[center_index]) / 2

    @cached_property_custom
    def mode(self) -> list[float | int]:
        """最頻値をリストで返します。"""
        # collections.Counter を使わずに実装
        if not self._values:
            return []

        freq = {}
        for value in self._values:
            # dict.get(key, default) を使い、キーが存在しない場合の初期値を0に設定
            freq[value] = freq.get(value, 0) + 1
        
        # max() は組み込み関数
        if not freq:
            return []
        max_cnt = max(freq.values())
        
        modes = []
        for k, v in freq.items():
            if v == max_cnt:
                modes.append(k)
        
        # sorted() は組み込み関数
        return sorted(modes)

    @cached_property_custom
    def variance(self) -> float:
        """不偏分散を返します。"""
        if self.size <= 1:
            return 0.0
        # sum() と ** 演算子は組み込み
        return sum((x - self.mean) ** 2 for x in self._values) / (self.size - 1)

    # -------- misc --------
    def __iter__(self) -> Iterable[float | int]:
        """ソートされた値のイテレータを返します。"""
        return iter(self._sorted)

    def __repr__(self) -> str:
        """オブジェクトの文字列表現を返します。"""
        return f"<NumberStats size={self.size} mean={self.mean:.3g}>"
    
s=NumberStats(1,2,3,4,5,6,7,8,9,10,1,1,1,1,10,10,10,10,10,10)
print(s)
