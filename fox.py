from animal import Animal
from species import Species
class Fox(Animal):
	def __init__(self, x, y):
		super().__init__(x, y)

		self._species = Species.Fox

		self.genes.sense = 70
		self.genes.speed = 3
		self.genes.size = 10
		
		self.definedSpeciesCheck()