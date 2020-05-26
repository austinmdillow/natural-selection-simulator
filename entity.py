from coord import Coord
class Entity:
	def __init__(self,x,y):
		self.x_pos = x
		self.y_pos = y
		self.size = 3
		self.isAlive = True

		self.coord = Coord(x, y, 0)