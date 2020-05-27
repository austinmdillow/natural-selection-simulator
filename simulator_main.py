print("Simulator")
VERSION = 0.1

import pygame, sys
from pygame.locals import *
from environment import Environment
from animal import Animal
from food import Food
from time import sleep
from species import Species

import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
WIDTH = 1000 #game window width
HEIGHT = 1000 #game window height
FPS = 300 # frames per second setting
TICKS_PER_DAY = FPS * 60000
NUM_ANIMALS_START = 100
NUM_FOOD_START = 100

fpsClock = pygame.time.Clock()
bunny_img = pygame.image.load('resources/cat.jpg')
walls = [] 

environment = Environment(NUM_ANIMALS_START,NUM_FOOD_START)



def draw_boundary(surface):
	pass #pygame.draw.walls[0]


def draw_actors(surface):
	surface.fill((0,0,0))
	for animal in environment.animals[Species.Rabbit]:
		x = animal.x_pos
		y = animal.y_pos

		pygame.draw.rect(surface, RED, (x, y, 1 * animal.size, 1 * animal.size))
		#print(.collide)

		if animal.detected == "plant":
			circle_color = GREEN
		else:
			circle_color = WHITE
		pygame.draw.circle(surface, circle_color, (int(x), int(y)), animal.genes["sense"],1)

	for plant in environment.plants[Species.Carrot]:
		x = plant.x_pos
		y = plant.y_pos
		size = plant.size
		pygame.draw.rect(surface, GREEN, (x, y, 1 * size, 1 * size))

def draw_stats(surface, font):
	text = font.render("Alive: " + str(len(environment.animals[Species.Rabbit])), True, GREEN, WHITE)
	text2 = font.render("FPS: " + str(FPS) + " " + str(int(fpsClock.get_fps())), True, GREEN, WHITE)
	surface.blit(text, (50,50))
	surface.blit(text2, (50,100))



def main():
	global FPS
	pygame.init()
	

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
			elif event.type == pygame.KEYDOWN:
				if event.key == K_UP:
					FPS += 5
				elif event.key == K_DOWN:
					FPS = max(0, FPS - 5)


		if ticks > TICKS_PER_DAY:
			pygame.quit()
			sys.exit()

		environment.update()
		draw_actors(Base_Surf)
		draw_boundary(Base_Surf)
		draw_stats(Base_Surf, font)

		pygame.display.update()
		fpsClock.tick(FPS)
		ticks += 1


if __name__ == '__main__':
	main()