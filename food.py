from entity import Entity
from genes import Genes
class Food(Entity):
	def __init__(self, x, y):
		super().__init__(x,y)
		self.genes = Genes(Genes.Plant)
		self.range = 10.0
		self.nutrients = 1.
		self.type = "food"

	def isAvailable(self):
		return self.nutrients > 0

	def eat(self, amount_wanted):
		amount_eaten = 0
		if amount_wanted < 0:
			print("Invalid eating amount")
			return 0

		if self.isAvailable():
			if amount_wanted < self.nutrients:
				self.nutrients -= amount_wanted
				amount_eaten = amount_wanted
			else:
				amount_eaten = self.nutrients # eat all the nutrients left
				self.nutrients = 0
				

		return amount_eaten

class Carrot(Food):
  def __init__(self, x, y):
    super().__init__(x, y)
