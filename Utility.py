from math import sqrt

# this is a vector class made for being used in pixel coordinates for the window
class Vector2:
    def __init__(self, x : int, y : int) -> None:
        self._x = x
        self._y = y
        self.magnitude = sqrt(self.x * self.x + self.y * self.y)
        pass

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.magnitude = sqrt(self.x * self.x + self.y * self.y)

    # @x.getter
    # def

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.magnitude = sqrt(self.x * self.x + self.y * self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector2(x, y)
    
    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other : int):
        return Vector2(self.x * other, self.y * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other : int):
        x = self.x / other
        y = self.y / other
        return Vector2(x, y)
    
    def __str__(self) -> str:
        return f'Vector2({self.x}, {self.y})'

    def AverageVector(vectors : list):
        totalVector = Vector2(0, 0)

        for vector in vectors:
            totalVector += vector

        return totalVector / len(vectors)