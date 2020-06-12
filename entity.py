from coord import Coord
from genes import Genes
class Entity:
	def __init__(self,x,y):
		self.genes = None # must be filled in later
		self.isAlive = True
		self.coord = Coord(x, y, 0)