from coord import Coord
class Entity:
	def __init__(self,x,y):
		self.size = 3
		self.isAlive = True

		self.coord = Coord(x, y, 0)