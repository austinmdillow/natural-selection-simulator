from agent import Agent
from species import Species
import math
import random
class Animal(Agent):
	WIDTH = 1000 #game window width
	HEIGHT = 1000 #game window height
	ENV = 0
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
			"hunger": .1,
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

		self.max_desire = "eat"
		self.is_alive = True
		self.speed = 60
		self.ticks_alive = 0
		self.dir = random.uniform(0,360)
		self.state = "explore"
		self.detected = "nothing"
		self.base_jitter = 1
		self.eat_range = 5

	def __str__(self):
		return "Animal name = " + str(id(self))
		#print("x , y = " + str(self.x_pos) + ", " + str(self.y_pos) )
		#print("Hunger: " + str(self.health["hunger"]))

	def closestPlant(self, env):
		target = None
		min_dist = 100000
		for plant in env.plants[Species.Carrot]:
			dist = self.distanceToAgent(plant)
			if (dist <= self.genes["sense"]):
				if (min_dist > dist): # if this is a new closest plant
					min_dist = dist
					target = plant
					print(min_dist)

		return target

	def healthChecks(self):
		self.ticks_alive = self.ticks_alive + 1
		self.health["thirst"] += .001 * self.genes["water_need"]
		self.health["hunger"] += .01
		#print(self.health["hunger"])
		if self.health["hunger"] > 3:
			self.state = "dead"
			return True
		else:
			return False

	def distanceToAgent(self, agent):
		return math.sqrt((agent.x_pos - self.x_pos)**2 + (agent.y_pos - self.y_pos)**2)



	def update(self, env):
		self.state = "explore"
		if self.healthChecks():
			return

		if True:
			self.dir = (self.dir + random.uniform(-self.base_jitter,self.base_jitter)) % 360
			target_plant = self.closestPlant(env)



			if (target_plant is not None): # this means that we found a plant

				self.dir = self.angle_to(target_plant.x_pos, target_plant.y_pos)
				self.detected = "plant"

				if (self.distanceToAgent(target_plant) <= self.eat_range):
					self.consume(env, target_plant)
				else:
					self.move()


			else:
				#print("None")
				if (self.health["hunger"] < .09) and (random.random() < .05):
					self.state = "reproduced"
				self.detected = "nothing"
				self.move()


	def move(self):

		norm = math.sqrt((math.cos(math.radians(self.dir)))**2 + (math.sin(math.radians(self.dir)))**2)
		x_tmp = self.x_pos + self.genes["speed"] * math.cos(math.radians(self.dir))/norm
		y_tmp = self.y_pos + self.genes["speed"] * math.sin(math.radians(self.dir))/norm
		#print(self.dir)

		if (x_tmp > self.WIDTH) or (x_tmp < 0):
			self.dir = (180 - self.dir) % 360
		if (y_tmp > self.HEIGHT) or (y_tmp < 0):
		 	self.dir = (-(self.dir)) % 360

		else:
			self.y_pos = y_tmp
			self.x_pos = x_tmp

	def consume(self, env, target):
		if target.isAvailable():
			self.health["hunger"] = max(0, self.health["hunger"] - target.eat(.05))
			print("Eating: " + str(self.health["hunger"]))
		else:
			print("not eating")




	def angle_to(self, x_tar, y_tar):
		return math.atan2(y_tar-self.y_pos, x_tar-self.x_pos) * 180 / math.pi

		# print(self.x_pos,self.y_pos)


