from typing import Union
from copy import deepcopy as dcp


class Point2D:
    def __init__(self, x: Union[float, int], y: Union[float, int]):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def coord(self):
        return [self._x, self._y]

    def __add__(self, other):
        assert isinstance(other, Point2D)
        pt = Point2D(self._x + other.x, self._y + other.y)
        return pt

    def __iadd__(self, other):
        assert isinstance(other, Point2D)
        self._x += other.x
        self._y += other.y
        return self

    def __sub__(self, other):
        assert isinstance(other, Point2D)
        pt = Point2D(self._x - other.x, self._y - other.y)
        return pt

    def __isub__(self, other):
        assert isinstance(other, Point2D)
        self._x -= other.x
        self._y -= other.y
        return self
