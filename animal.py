from entity import Entity
from species import Species
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

		self._sex = random.choice(['m', 'f'])

		self._is_alive = True
		self.speed = 60
		self.ticks_alive = 0
		self.dir = random.uniform(0,360)
		self.state = "explore"
		self.detected = "nothing"
		self.base_jitter = 1
		self.eat_range = 5

		self.tickstoDeathMovement = 400
		self.tickstoDeathHunger = 200
		self.lastReproductionTime = 400

	def __str__(self):
		return "Animal name = " + str(id(self))
		#print("x , y = " + str(self.x_pos) + ", " + str(self.y_pos) )
		#print("Hunger: " + str(self.health["hunger"]))

	def healthChecks(self):
		self.ticks_alive = self.ticks_alive + 1
		self.health["thirst"] += .001 * self.genes["water_need"]
		self.health["hunger"] += 1 / self.tickstoDeathHunger
		self.health["reproductive_urge"] = min(self.health["reproductive_urge"]+ .01, 0.5)

		#print(self.health["hunger"])
		if self.health["hunger"] > 3:
			self.state = "dead"
			return True
		else:
			return False

	def distanceToAgent(self, agent):
		return math.sqrt((agent.x_pos - self.x_pos)**2 + (agent.y_pos - self.y_pos)**2)

	def getDesire(self):
		self.desires["eat"] = self.health["hunger"]
		self.desires["sleep"] = self.health["tiredness"]
		self.desires["reproduce"] = 0 if self.desires["eat"] > .3 or self.desires["sleep"] >.3 or (self.ticks_alive - self.lastReproductionTime <= 400)  else self.health["reproductive_urge"]
		max_desire = max(self.desires, key=self.desires.get)
		print("Max Desire = " + max_desire)

		return(max_desire)


	def update(self, env):
		self.state = "explore"
		if self.healthChecks():
			return

		current_desire = self.getDesire()

		if current_desire == "eat":
			self.findFood(env)
		
		elif current_desire == "reproduce":
			self.reproduce()

		elif current_desire == "sleep":
			self.sleep()

		else: # we go exploring
			self.explore()
			


	def move(self):

		norm = math.sqrt((math.cos(math.radians(self.dir)))**2 + (math.sin(math.radians(self.dir)))**2)
		x_tmp = self.x_pos + self.genes["speed"] * math.cos(math.radians(self.dir))/norm
		y_tmp = self.y_pos + self.genes["speed"] * math.sin(math.radians(self.dir))/norm
		#print(self.dir)

		# handle collisions
		if (x_tmp > self.WIDTH) or (x_tmp < 0):
			self.dir = (180 - self.dir) % 360
		if (y_tmp > self.HEIGHT) or (y_tmp < 0):
		 	self.dir = (-(self.dir)) % 360

		else:
			self.y_pos = y_tmp
			self.x_pos = x_tmp
		
		self.coord.updateXY(self.x_pos, self.y_pos)
		
		self.health["tiredness"] += self.genes["speed"] / self.tickstoDeathMovement

	def explore(self):
		self.dir = (self.dir + random.uniform(-self.base_jitter,self.base_jitter)) % 360
		self.move()


	def angle_to(self, x_tar, y_tar):
		return math.atan2(y_tar-self.y_pos, x_tar-self.x_pos) * 180 / math.pi


	### Actions to take

	def findFood(self, env):
		target_plant = env.sense(self).closest_plant

		if (target_plant is not None): # this means that we found a plant

			self.dir = self.angle_to(target_plant.x_pos, target_plant.y_pos)
			self.detected = "plant"

			if (self.distanceToAgent(target_plant) <= self.eat_range):
				self.consume(env, target_plant)
			else:
				self.move()
		else:
			self.detected = "nothing"
			self.explore()


	def consume(self, env, target):
		if target.isAvailable():
			self.health["hunger"] = max(0, self.health["hunger"] - target.eat(.2))
			print("Eating: " + str(self.health["hunger"]))
		else:
			print("not eating")



	def reproduce(self):
		if (random.random() < .01):
			self.lastReproductionTime = self.ticks_alive
			print("WE MADE A BABY")
			self.state = "reproduced"
			self.health["reproductive_urge"] = 0

	def sleep(self):
		# we don't do anything except decrease the tiredness

		self.health["tiredness"] = max(0, self.health["tiredness"] - (1 / self.tickstoDeathMovement) * 3)