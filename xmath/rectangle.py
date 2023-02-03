from typing import Union

# from point2d import Point2D


class Rect:
    def __init__(self,
                 l_x: Union[float, int],
                 t_y: Union[float, int],
                 r_x: Union[float, int] = None,
                 b_y: Union[float, int] = None,
                 w: Union[float, int] = None,
                 h: Union[float, int] = None,
                 ):
        assert (r_x is None and b_y is None and isinstance(w, (float, int)) and isinstance(h, (float, int))) or \
               (isinstance(r_x, (float, int)) and isinstance(b_y, (float, int)) and w is None and h is None)
        self._l_x = float(l_x)
        self._t_y = float(t_y)

        self._r_x = float(r_x) if r_x is not None else float(l_x + w)
        self._b_y = float(b_y) if b_y is not None else float(t_y + h)

        self._w = float(w) if w is not None else float(r_x - l_x)
        self._h = float(h) if h is not None else float(b_y - t_y)

        self._c_x = self._l_x + float(self._w / 2)
        self._c_y = self._t_y + float(self._h / 2)

    # top, left
    @property
    def l_x(self) -> float:
        return self._l_x

    @property
    def t_y(self) -> float:
        return self._t_y

    @property
    def top_left(self) -> list:
        return [self._l_x, self._t_y]

    # bottom, right
    @property
    def r_x(self) -> float:
        return self._r_x

    @property
    def b_y(self) -> float:
        return self._b_y

    @property
    def bottom_right(self) -> list:
        return [self._r_x, self._b_y]

    # center
    @property
    def c_x(self) -> float:
        return self._c_x

    @property
    def c_y(self) -> float:
        return self._c_y

    @property
    def center(self) -> list:
        return [self._c_x, self._c_y]

    # width, height
    @property
    def width(self) -> float:
        return self._w

    @property
    def height(self) -> float:
        return self._h

    @property
    def width_height(self) -> list:
        return [self._w, self._h]

    # bboxes
    @property
    def xywh(self) -> list:
        return [self._l_x, self._t_y, self._w, self._h]

    @property
    def xyxy(self) -> list:
        return [self._l_x, self._t_y, self._r_x, self._b_y]

    @property
    def ccwh(self) -> list:
        return [self._c_x, self._c_y, self._w, self._h]

    @property
    def area(self) -> float:
        return self._w * self._h

    # keys
    def is_pt_in(self, pt: list) -> bool:
        assert isinstance(pt, list) and len(pt) == 2 and \
               isinstance(pt[0], (float, int)) and isinstance(pt[1], (float, int))
        return self._l_x <= pt[0] <= self._r_x and self._t_y <= pt[1] <= self._b_y

    def iou(self, other) -> float:
        assert isinstance(other, Rect)
        l_x = max(self.l_x, other.l_x)
        r_x = min(self.r_x, other.r_x)
        t_y = max(self.t_y, other.t_y)
        b_y = min(self.b_y, other.b_y)

        w = max((r_x - l_x), 0)
        h = max((b_y - t_y), 0)

        intersection_area = w * h

        return intersection_area / float(self.area + other.area - intersection_area)

    def __str__(self):
        return f"{self.xywh}"
