from __future__ import annotations
from typing import Tuple


class Vector(object):
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y


class Point(object):
    def __init__(self, x: float, y: float):
        self.X = x
        self.Y = y

    def __str__(self) -> str:
        print(f"X, Y = {self.X}, {self.Y}")

    def __add__(self, p: Vector) -> Point:
        return Point(self.X + p.X, self.Y + p.Y)

    def to_tuple(self) -> Tuple[float, float]:
        return (self.X, self.Y)
