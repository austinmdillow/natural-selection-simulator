import math


class Coord:
    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def __str__(self):
        return "X: {0}, Y: {1}, D: {2}".format(self.x, self.y, self.dir)

    def update(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir

    def updateXY(self, x, y):
        self.x = x
        self.y = y

    def angle2Coord(self, coord2):
        return math.atan2(coord2.y - self.y, coord2.x - self.x) * 180 / math.pi

    def distanceToCoord(self, coord2):
        return math.sqrt((coord2.x - self.x) ** 2 + (coord2.y - self.y) ** 2)
