from species import Species
from animal import Animal
from fox import Fox
from rabbit import Rabbit
from food import *
from time import sleep
from surroundings import Surroundings
import random
import math

class Environment:
  debug = True
  ticks = 0
  animals = {
    Species.Fox: [],
    Species.Rabbit: []
  }

  plants = {
    Species.Carrot: []
  }

  def __init__(self, animal_start, plant_start, height, width):
    self.height = height
    self.width = width
    Animal.HEIGHT = height
    Animal.WIDTH = width
    self.animals_alive = 123
    for i in range(animal_start):
      self.animals[Species.Rabbit].append(Rabbit(random.uniform(50, self.width - 50), random.uniform(50, self.height - 50)))
      
    for i in range(plant_start):
      self.plants[Species.Carrot].append(Carrot(random.uniform(50, self.width - 50),random.uniform(50, self.height - 50)))

    
    self.animals[Species.Fox].append(Fox(random.uniform(50, self.width - 50), random.uniform(50, self.height - 50)))

  def distanceToAgent(self, agent1, agent2):
    return math.sqrt((agent2.coord.x - agent1.coord.x)**2 + (agent2.coord.y - agent1.coord.y)**2)

  

  def sense(self, animal_base):
    surrounding_res = Surroundings()
    for spec in self.animals.keys():
      for animal2 in self.animals[spec]:
        animal2_dist = self.distanceToAgent(animal_base, animal2)
        if (animal2_dist < animal_base.genes.sense):
          if Species.predator(animal_base._species) == animal2._species:
            surrounding_res.closest_predator = animal2
            surrounding_res.closest_predator_dist = animal2_dist

          elif Species.prey(animal_base._species) == animal2._species:
            surrounding_res.closest_prey = animal2
            surrounding_res.closest_prey_dist = animal2_dist

    for spec in self.plants.keys():
      for plant in self.plants[spec]:
        plant_dist = self.distanceToAgent(animal_base, plant)
        if (plant_dist < animal_base.genes.sense):
          if (surrounding_res.closest_plant is None or plant_dist < surrounding_res.closest_plant_dist):
            surrounding_res.closest_plant = plant
            surrounding_res.closest_plant_dist = plant_dist


    return surrounding_res

  
  def closestAnimal(self, coord):
    temp_dist = None
    temp_animal = None
    for spec in self.animals.keys():
      for animal in self.animals[spec]:
        dist = coord.distanceToCoord(animal.coord)

        if (temp_animal is None):
          temp_dist = dist
          temp_animal = animal
        elif dist < temp_dist:
          temp_dist = dist
          temp_animal = animal
    
    return temp_animal



    



  def update(self):
    self.ticks+=1


    if self.ticks % 10 == 0:
      self.plants[Species.Carrot].append(Food(random.uniform(50, self.width - 50),random.uniform(50, self.height - 50)))


    for spec in self.animals.keys():
      for animal in self.animals[spec]:
        animal.update(self)
        if animal.state == "dead":
          self.animals[spec].remove(animal)
        elif animal.state == "reproduced":
          if animal._species == Species.Rabbit:
            self.animals[spec].append(Rabbit(animal.coord.x, animal.coord.y))
          elif animal._species == Species.Fox:
            self.animals[spec].append(Fox(animal.coord.x, animal.coord.y))
    

    for spec in self.plants.keys():
      for plant in self.plants[spec]:
        if not plant.isAvailable():
          self.plants[spec].remove(plant)


