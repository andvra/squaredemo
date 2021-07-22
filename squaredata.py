from collections.abc import MutableSequence
import array
from utils import Point


class SquareData:
    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point, p5: Point, side_length: float, angle: float):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.p5 = p5
        self.side_length = side_length
        self.angle = angle

    def as_array(self) -> MutableSequence[float]:
        return array.array('f', [
            *self.p1.to_tuple(),
            *self.p2.to_tuple(),
            *self.p3.to_tuple(),
            *self.p4.to_tuple(),
            *self.p5.to_tuple(),
            self.side_length,
            self.angle
        ])
