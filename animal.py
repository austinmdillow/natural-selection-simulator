from entity import Entity
from species import Species
from genes import Genes
import math
import random
import time

class Animal(Entity):
	WIDTH = 1000 #game window width
	HEIGHT = 1000 #game window height

	def __init__(self, x, y):
		super().__init__(x, y)

		self.genes = {
			"sense": 50,
			"speed": 5.0,
			"size": 3.0,
			"water_need": 1.0
		}

		self.genes = Genes()


		self.health = {
			"thirst": .1,
			"hunger": .5,
			"reproductive_urge": .1,
			"tiredness": .1
		}

		
		self.desires = {
			"eat": 0,
			"drink": 0,
			"sleep": 0,
			"reproduce": 0,
			"evade": 0
		}
		self._debug = False

		self._sex = random.choice(['m', 'f'])
		self._species = None # IMPLEMENT AT A LOWER LEVEL

		self._is_alive = True
		self.speed = 60
		self.ticks_alive = 0
		self.dir = random.uniform(0,360)
		self.state = "explore"
		self.detected = "nothing"
		self.base_jitter = 1
		self.eat_range = 5
		self.lastAction = "nothing"


		self.tickstoDeathMovement = 400
		self.tickstoDeathHunger = 400
		self.lastReproductionTime = 400

	def __str__(self):
		return "Animal name = " + str(id(self))
		#print("x , y = " + str(self.x_pos) + ", " + str(self.y_pos) )
		#print("Hunger: " + str(self.health["hunger"]))
	
	def printDebug(self):
		print(self.coord)
		for k, v in self.health.items():
			print(str(k) + ": %.2f"%v, end =". ")
		print()
		for k, v in self.desires.items():
			print(str(k) + ": %.2f"%v, end =". ")
		print()
		print("Last Action = " + self.lastAction)
	
	def definedSpeciesCheck(self):
		print(self._species)
		if self._species == None:
			raise Exception("Need to define species")

	def healthChecks(self):
		self.ticks_alive = self.ticks_alive + 1
		self.health["thirst"] += .001
		self.health["hunger"] += 1 / self.tickstoDeathHunger
		self.health["reproductive_urge"] = min(self.health["reproductive_urge"]+ .01, 0.5)

		#print(self.health["hunger"])
		if self.health["hunger"] > 3:
			self.state = "dead"
			return True
		else:
			return False

	def getDesire(self, env, surroundings):

		

		self.desires["eat"] = self.health["hunger"]
		self.desires["sleep"] = self.health["tiredness"]
		self.desires["reproduce"] = 0 if self.desires["eat"] > .3 or self.desires["sleep"] >.3 or (self.ticks_alive - self.lastReproductionTime <= 400)  else self.health["reproductive_urge"]
		self.desires["evade"] = 0 if surroundings.closest_predator is None else 1
		
		max_desire = max(self.desires, key=self.desires.get)
		# print("Max Desire = " + max_desire)

		return(max_desire)


	def update(self, env):
		self.state = "explore"
		if self.healthChecks():
			return

		surroundings = env.sense(self)
		current_desire = self.getDesire(env, surroundings)

		if current_desire == "eat":
			self.findFood(env)
		
		elif current_desire == "reproduce":
			self.reproduce()

		elif current_desire == "sleep":
			self.sleep()
		
		elif current_desire == "evade":
			self.evade(surroundings.closest_predator)
			self.lastAction = current_desire

		else: # we go exploring
			self.explore()
		
		self.lastAction = current_desire
			


	def move(self):

		norm = math.sqrt((math.cos(math.radians(self.coord.dir)))**2 + (math.sin(math.radians(self.coord.dir)))**2)
		x_tmp = self.coord.x + self.genes.speed * math.cos(math.radians(self.coord.dir))/norm
		y_tmp = self.coord.y + self.genes.speed * math.sin(math.radians(self.coord.dir))/norm
		#print(self.dir)

		# handle collisions
		if (x_tmp > self.WIDTH) or (x_tmp < 0):
			self.coord.dir = (180 - self.coord.dir) % 360
		if (y_tmp > self.HEIGHT) or (y_tmp < 0):
		 	self.coord.dir = (-(self.coord.dir)) % 360

		else:
			self.coord.updateXY(x_tmp, y_tmp)
		
		
		
		# TODO add this back in
		# self.health["tiredness"] += self.genes["speed"] / self.tickstoDeathMovement

	def explore(self):
		self.dir = (self.dir + random.uniform(-self.base_jitter,self.base_jitter)) % 360
		self.move()



	### Actions to take

	def findFood(self, env):
		target_plant = env.sense(self).closest_plant

		if (target_plant is not None): # this means that we found a plant

			self.coord.dir = self.coord.angle2Coord(target_plant.coord)
			self.detected = "plant"

			if (env.distanceToAgent(self, target_plant) <= self.eat_range):
				self.consume(env, target_plant)
			else:
				self.move()
		else:
			self.detected = "nothing"
			self.explore()


	def consume(self, env, target):
		if target.isAvailable():
			self.health["hunger"] = max(0, self.health["hunger"] - target.eat(.2))
			#print("Eating: " + str(self.health["hunger"]))
		else:
			#print("not eating")
			pass


	def reproduce(self):
		if (random.random() < .01):
			self.lastReproductionTime = self.ticks_alive
			print("WE MADE A BABY")
			self.state = "reproduced"
			self.health["reproductive_urge"] = 0

	def sleep(self):
		# we don't do anything except decrease the tiredness

		self.health["tiredness"] = max(0, self.health["tiredness"] - (1 / self.tickstoDeathMovement) * 3)

	
	def evade(self, predator):
		if self._debug:
			print(predator)
			print(predator.coord)
			print(self.coord.angle2Coord(predator.coord))
		self.coord.dir = self.coord.angle2Coord(predator.coord) + 180
		self.move()