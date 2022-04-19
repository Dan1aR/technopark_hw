""" Custom list implementaion """
from operator import add


class CustomList(list):
    """ List with emphasis on summation """
    def __str__(self):
        return f"{super().__str__()} {sum(self.copy())}"

    def __add__(self, other):
        size = self.__len__() - len(other)
        shift = []
        if size > 0:
            shift = self.copy()[-size:]
        elif size < 0:
            shift = other[size:]
        return CustomList(list(map(add, self.copy(), other)) + shift)

    def __sub__(self, other):
        return self.__add__(list(map(lambda x: x * -1, other)))

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        return CustomList(map(lambda x: x * -1, self.__sub__(other)))

    def __eq__(self, other):
        return sum(self.copy()) == sum(other)

    def __ne__(self, other):
        return sum(self.copy()) != sum(other)

    def __lt__(self, other):
        return sum(self.copy()) < sum(other)

    def __le__(self, other):
        return sum(self.copy()) <= sum(other)

    def __gt__(self, other):
        return sum(self.copy()) > sum(other)

    def __ge__(self, other):
        return sum(self.copy()) >= sum(other)
