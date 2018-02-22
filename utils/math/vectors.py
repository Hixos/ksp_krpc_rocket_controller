import math


class Vector3:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

    @staticmethod
    def fromTuple(t):
        """
        Returns a vector generated from data in the specified tuple
        :param t: the tuple
        :return: Vector from tuple
        """
        return Vector3(t[0], t[1], t[2])

    def magnitude(self):
        return math.sqrt(math.pow(self.X, 2) + math.pow(self.Y, 2) + math.pow(self.Z, 2))

    def __add__(self, other):
        return Vector3(self.X + other.X, self.Y + other.Y, self.Z + other.Z)
