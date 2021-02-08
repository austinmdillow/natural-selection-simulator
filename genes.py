import random


class Genes:
    mutation = False
    Animal = 0
    Plant = 1

    def __init__(self, entity_type):
        self.size = 5  # default value
        self.typeSpecificTraits(entity_type)

    def typeSpecificTraits(self, entity_type):
        if entity_type == Genes.Animal:
            self.sense = 50
            self.speed = 10
            self.strength = 3
            self.defense = 1
        elif entity_type == Genes.Plant:
            pass

    def printDebug(self):
        print("Sense = " + str(self.sense) + ", Speed = " + str(self.speed))

    @staticmethod
    def combineGenes(g1, g2):
        g3 = Genes(Genes.Animal)

        g3.sense = random.choice([g1.sense, g2.sense]) * random.uniform(0.9, 1.1)
        g3.speed = random.choice([g1.speed, g2.speed]) * random.uniform(0.9, 1.1)
        g3.strength = random.choice(
            [g1.strength, g2.strength]
        )  # * random.uniform(.9,1.1)
        g3.defense = random.choice([g1.defense, g2.defense])  # * random.uniform(.9,1.1)

        g1.printDebug()
        g3.printDebug()
        return g3
