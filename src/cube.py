from vec import Vec


class Cube:
    """
    平顶六边形 flat==True:
    r 轴: 指向屏幕正右方
    g 轴: 指向屏幕左上方与水平面呈 60° 角
    b 轴: 指向屏幕左下方与水平面呈 60° 角
    尖顶六边形 flat==False:
    r 轴: 指向屏幕正上方
    g 轴: 指向屏幕左下方与水平面呈 30° 角
    b 轴: 指向屏幕右下方与水平面呈 30° 角
    """

    CUBE_SIDES = None

    def __init__(self, r=(0, 0, 0), g=None, b=None):
        if g is None:
            self.__init__(*r)
            return
        if b is None:
            self.__init__(r, g, -r - g)
            return
        assert abs(r + g + b) <= 1e-12, "r + g + b must be 0"
        self._r, self._g, self._b = r, g, b

    def __repr__(self):
        return "cube(%s,%s,%s)" % (self._r, self._g, self._b)

    def __str__(self):
        return "(%s,%s,%s)" % (self._r, self._g, self._b)

    def __getitem__(self, key):
        if key == 0 or key == -3:
            return self._r
        if key == 1 or key == -2:
            return self._g
        if key == 2 or key == -1:
            return self._b
        raise IndexError

    def __len__(self):
        return 3

    def __add__(self, other):
        if isinstance(other, Cube):
            return Cube(*[self[i] + other[i] for i in range(3)])
        else:
            return self + Cube(other)

    def __radd__(self, other):
        return other + self

    def __neg__(self):
        return Cube(*[-i for i in self])

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Cube(*[other * i for i in self])

    def __rmul__(self, other):
        return other * self

    def __abs__(self):
        return sum(map(abs, self)) // 2

    def __eq__(self, other):
        if isinstance(other, Cube):
            return False not in list(map(lambda x, y: x == y, self, other))

    def rot_cw(self):
        return Cube(*[-self[i] for i in range(-1, 2)])

    def rot_ccw(self):
        return Cube(*[-self[i] for i in range(-2, 1)])

    def round(self):
        """
        四舍五入到最近的整数坐标
        """
        val = list(map(lambda x: int(x + 0.5) if x > 0 else int(x - 0.5), self))
        dif = list(map(lambda x, y: abs(x - y), val, self))
        val[dif.index(max(dif))] = (-val[dif.index(max(dif)) - 1] - val[dif.index(max(dif)) - 2])
        return Cube(val)

    def to_pixel(self, flat=True, y_rev=False):
        """
        返回这样一个坐标, 它的x轴正向指向屏幕正右侧, y轴正向指向屏幕正上方
        """
        sign = -1 if y_rev else 1
        if flat:
            return Vec(3 / 2 * self[0], sign * (3 ** 0.5) * (self[0] / 2 + self[1]))
        else:
            return Vec((self[0] + self[1] / 2) * (3 ** 0.5), sign * 3 / 2 * self[1])


def to_cube(pos, flat=True, y_rev=False):
    """
    返回一个六边形坐标
    """
    sign = -1 if y_rev else 1
    if flat:
        return Cube(2 / 3 * pos[0], (sign * pos[1] * (3 ** 0.5) - 1 * pos[0]) / 3)
    else:
        return Cube(((3 ** 0.5) * pos[0] - sign * pos[1]) / 3, 2 / 3 * sign * pos[1])


N, NE, SE, S, SW, NW = (
    Cube(0, 1, -1),
    Cube(1, 0, -1),
    Cube(1, -1, 0),
    Cube(0, -1, 1),
    Cube(-1, 0, 1),
    Cube(-1, 1, 0),
)
CUBE_SIDES = (N, NE, SE, S, SW, NW)
