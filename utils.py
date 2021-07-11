from __future__ import annotations
import math


class Vector(object):
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y

    def norm(self) -> float:
        return math.hypot(self.X, self.Y)

    def normals(self) -> tuple[Vector, Vector]:
        return (Vector(-self.Y, self.X), Vector(self.Y, -self.X))

    def __mul__(self, n: float) -> Vector:
        return Vector(self.X*n, self.Y*n)

    def __rmul__(self, n: float) -> Vector:
        return self.__mul__(n)

    def unit(self) -> Vector:
        norm = self.norm()
        norm = max(norm, 0.000001)  # Avoid division by zero
        return Vector(self.X / norm, self.Y / norm)

    def __str__(self) -> str:
        return f"X,Y = {self.X}, {self.Y}"

    def angle(self) -> float:
        return math.atan2(self.Y, self.X)


class Point(object):
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y

    def __str__(self) -> str:
        return f"X, Y = {self.X}, {self.Y}"

    def __add__(self, v: Vector) -> Point:
        return Point(self.X + v.X, self.Y + v.Y)

    def __sub__(self, p: Point) -> Vector:
        return Vector(self.X - p.X, self.Y - p.Y)

    def to_tuple(self) -> tuple[float, float]:
        return (self.X, self.Y)
