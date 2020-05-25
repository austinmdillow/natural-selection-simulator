print("Simulator")
VERSION = 0.1

import pygame, sys
from pygame.locals import *
from animal import Animal
from food import Food
from time import sleep
import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
WIDTH = 1000 #game window width
HEIGHT = 1000 #game window height
FPS = 300 # frames per second setting
TICKS_PER_DAY = FPS * 60
NUM_ANIMALS_START = 10
NUM_FOOD_START = 30

fpsClock = pygame.time.Clock()
bunny_img = pygame.image.load('resources/cat.jpg')
animals_alive = []
plant_list = []
animal_test = Animal(100,100)
Environment = {"animals_alive": animals_alive, "plant_list": plant_list}
walls = []



def update_environment():
	for animal in Environment["animals_alive"]:
		animal.update(Environment)
		if animal.state == "dead":
			Environment["animals_alive"].remove(animal)
		elif animal.state == "reproduced":
			print(str(id(animal)) + " created an offspring")
			addAnimal(animal.x_pos, animal.y_pos);

def draw_boundary(surface):
	pass #pygame.draw.walls[0]

def init_environment(num_animals, num_plants):

	init_animals(num_animals)
	init_food(num_plants)


def draw_actors(surface):
	surface.fill((0,0,0))
	for animal in Environment["animals_alive"]:
		x = animal.x_pos
		y = animal.y_pos

		pygame.draw.rect(surface, RED, (x, y, 1 * animal.size, 1 * animal.size))
		#print(.collide)

		if animal.detected == "plant":
			circle_color = GREEN
		else:
			circle_color = WHITE
		pygame.draw.circle(surface, circle_color, (int(x), int(y)), animal_test.genes["sense"],1)

	for i in range(len(plant_list)):
		x = plant_list[i].x_pos
		y = plant_list[i].y_pos
		size = plant_list[i].size
		pygame.draw.rect(surface, GREEN, (x, y, 1 * size, 1 * size))

def draw_stats(surface, font):
	text = font.render(str(len(Environment["animals_alive"])), True, GREEN, WHITE)
	surface.blit(text, (50,50))

def addAnimal(x, y):
	animals_alive.append(Animal(x, y))

def init_animals(number):
	for i in range(number):
		animals_alive.append(Animal(random.uniform(50, WIDTH - 50), random.uniform(50, HEIGHT - 50)))


	for i in range(len(animals_alive)):
		pass
		#print(animals_alive[i])
		#print(id(animals_alive[i]))

def init_food(number):
	for i in range(number):
		plant_list.append(Food(random.uniform(50, WIDTH - 50),random.uniform(50, HEIGHT - 50)))


def main():
	pygame.init()
	init_environment(NUM_ANIMALS_START, NUM_FOOD_START)
	#sleep(2)

	Base_Surf = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
	walls.append(pygame.Rect(0, 0, WIDTH, 1))

	pygame.display.set_caption("Evolution Simulator Version " + str(VERSION))
	font = pygame.font.SysFont("ubuntu", 24) 

	ticks = 0

	while True: # main game loop
		
		
		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYUP:
				sleep(2)

		if ticks % 10 == 0:
			plant_list.append(Food(random.uniform(50, WIDTH - 50),random.uniform(50, HEIGHT - 50)))


		if ticks > TICKS_PER_DAY:
			pygame.quit()
			sys.exit()

		update_environment()
		draw_actors(Base_Surf)
		draw_boundary(Base_Surf)
		draw_stats(Base_Surf, font)
		# Base_Surf.blit(bunny_img,(300+i,300))


		pygame.display.update()
		fpsClock.tick(FPS)
		#print(fpsClock.get_fps())
		ticks += 1


if __name__ == '__main__':
	main()