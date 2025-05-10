import math


class Vec(tuple):
    def __new__(cls, x=(0, 0), y=None):
        if y is None:
            return cls.__new__(cls, *x)
        return tuple.__new__(cls, (x, y))

    def __add__(self, other):
        return Vec(self[0] + other[0], self[1] + other[1])

    def __mul__(self, other):
        if isinstance(other, Vec):
            return self[0] * other[0] + self[1] * other[1]
        return Vec(self[0] * other, self[1] * other)

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vec(self[0] * other, self[1] * other)

    def __sub__(self, other):
        return Vec(self[0] - other[0], self[1] - other[1])

    def __neg__(self):
        return Vec(-self[0], -self[1])

    def __abs__(self):
        return (self[0] ** 2 + self[1] ** 2) ** 0.5

    def rotate(self, angle):
        """
        rotate self counterclockwise by angle
        """
        per = Vec(-self[1], self[0])
        angle = angle * math.pi / 180.0
        c, s = math.cos(angle), math.sin(angle)
        return Vec(self[0] * c + per[0] * s, self[1] * c + per[1] * s)

    def __getnewargs__(self):
        return self[0], self[1]

    def __repr__(self):
        return "(%s,%s)" % self

    def to_pixel(self):
        return self


N, E, S, W = (Vec(0, 1), Vec(1, 0), Vec(0, -1), Vec(-1, 0))
VEC_SIDES = (N, E, S, W)
