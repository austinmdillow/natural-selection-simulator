from species import Species
from animal import Animal
from food import Food
from time import sleep
from surroundings import Surroundings
import random
import math

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

  def distanceToAgent(self, agent1, agent2):
    return math.sqrt((agent1.x_pos - self.x_pos)**2 + (agent.y_pos - self.y_pos)**2)

  def distanceToCoord(self, coord1, coord2):
    return math.sqrt((coord2.x - coord1.x)**2 + (coord2.y - coord1.y)**2)

  def sense(self, coord, species):
    surrounding_res = Surroundings()
    for spec in self.animals.keys():
      for animal in self.animals[spec]:
        pass

    for spec in self.plants.keys():
      for plant in self.plants[spec]:
        plant_dist = self.distanceToCoord(coord, plant.coord)
        if (surrounding_res.closest_plant is None):
          if (plant_dist < 50): # TODO FIX
            surrounding_res.closest_plant = plant
            surrounding_res.closest_plant_dist = plant_dist

        elif (plant_dist < surrounding_res.closest_plant_dist):
          surrounding_res.closest_plant = plant
          surrounding_res.closest_plant_dist = plant_dist


    return surrounding_res

    



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