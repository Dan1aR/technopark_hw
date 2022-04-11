""" Custom list implementaion """
from operator import add, sub


class CustomList(list):
    """ List with emphasis on summation """
    def __str__(self):
        return f"{super().__str__()} {sum(super().copy())}"

    def _agg_util(self, agg_func, other):
        size = super().__len__() - len(other)
        shift = super().copy()[-size:] if size > 0 else other[size:]
        return CustomList(list(map(agg_func, super().copy(), other)) + shift)

    def __add__(self, other):
        return self._agg_util(add, other)

    def __sub__(self, other):
        return self._agg_util(sub, other)

    def __eq__(self, other):
        return sum(super().copy()) == sum(other)

    def __ne__(self, other):
        return sum(super().copy()) != sum(other)

    def __lt__(self, other):
        return sum(super().copy()) < sum(other)

    def __le__(self, other):
        return sum(super().copy()) <= sum(other)

    def __gt__(self, other):
        return sum(super().copy()) > sum(other)

    def __ge__(self, other):
        return sum(super().copy()) >= sum(other)
