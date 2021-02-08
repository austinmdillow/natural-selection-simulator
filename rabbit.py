from animal import Animal
from species import Species


class Rabbit(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        self._species = Species.Rabbit
        self.genes.size = 5

        self.definedSpeciesCheck()
