from species import Species
from animal import Animal
from food import Food
from time import sleep
import random

class Environment:
  WIDTH = 1000 #game window width
  HEIGHT = 1000 #game window height
  debug = True
  ticks = 0
  animals = {
    Species.Fox: [],
    Species.Rabbit: []
  }

  plants = {
    Species.Carrot: []
  }

  def sense(self, x,y, Species):
    pass

  def update(self):
    self.ticks+=1


    if self.ticks % 5 == 0:
      self.plants[Species.Carrot].append(Food(random.uniform(50, self.WIDTH - 50),random.uniform(50, self.HEIGHT - 50)))


    for spec in self.animals.keys():
      for animal in self.animals[spec]:
        animal.update(self)
        if animal.state == "dead":
          self.animals[Species.Rabbit].remove(animal)
        elif animal.state == "reproduced":
          self.animals[Species.Rabbit].append(Animal(animal.x_pos, animal.y_pos))
    

    for spec in self.plants.keys():
      for plant in self.plants[spec]:
        if not plant.isAvailable():
          self.plants[spec].remove(plant)


  def __init__(self, animal_start, plant_start):
    self.animals_alive = 123
    for i in range(animal_start):
      self.animals[Species.Rabbit].append(Animal(random.uniform(50, self.WIDTH - 50), random.uniform(50, self.HEIGHT - 50)))
    
    for i in range(plant_start):
      self.plants[Species.Carrot].append(Food(random.uniform(50, self.WIDTH - 50),random.uniform(50, self.HEIGHT - 50)))