print("Simulator")
VERSION = 0.1

import pygame, sys
from pygame.locals import *
from environment import Environment
from animal import Animal
from coord import Coord
from food import Food
from time import sleep
from species import Species

import random

RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
WIDTH = 1500 #game window width
HEIGHT = 1000 #game window height
FPS = 10 # frames per second setting
TICKS_PER_DAY = FPS * 6000
NUM_ANIMALS_START = 1
NUM_FOOD_START = 100

fpsClock = pygame.time.Clock()
bunny_img = pygame.image.load('resources/cat.jpg')
walls = [] 
environment = Environment(NUM_ANIMALS_START,NUM_FOOD_START, HEIGHT, WIDTH)



def draw_boundary(surface):
	pass #pygame.draw.walls[0]


def draw_actors(surface, selected_animal):
	surface.fill((0,0,0))

	for animal in environment.animals[Species.Fox]:
		x = animal.coord.x
		y = animal.coord.y
		animal_color = YELLOW

		if animal == selected_animal:
			animal_color = BLUE
		pygame.draw.rect(surface, animal_color, (x, y, 1 * animal.size, 1 * animal.size))
		#print(.collide)

		if animal.detected == "plant":
			circle_color = GREEN
		else:
			circle_color = WHITE
		pygame.draw.circle(surface, circle_color, (int(x), int(y)), animal.genes.sense,1)

	for animal in environment.animals[Species.Rabbit]:
		x = animal.coord.x
		y = animal.coord.y
		animal_color = RED

		if animal == selected_animal:
			animal_color = BLUE

		pygame.draw.rect(surface, animal_color, (x, y, 1 * animal.size, 1 * animal.size))
		#print(.collide)

		if animal.detected == "plant":
			circle_color = GREEN
		else:
			circle_color = WHITE
		pygame.draw.circle(surface, circle_color, (int(x), int(y)), animal.genes.sense,1)

	for plant in environment.plants[Species.Carrot]:
		x = plant.coord.x
		y = plant.coord.y
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
	is_paused = False
	selected_animal = None

	while True: # main game loop
		
		if ticks > TICKS_PER_DAY:
			pygame.quit()
			sys.exit()

		for event in pygame.event.get():

			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == K_UP:
					FPS += 5
				elif event.key == K_DOWN:
					FPS = max(0, FPS - 5)
				elif event.key == K_c:
					selected_animal._debug = False
					selected_animal = None
				elif event.key == K_SPACE:
					is_paused = not is_paused
					
			
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if selected_animal is not None:
					selected_animal._debug = False
				(x_mouse, y_mouse) = pygame.mouse.get_pos()
				print("CLICKED " + str(x_mouse) + " " + str(y_mouse))
				selected_animal = environment.closestAnimal(Coord(x_mouse, y_mouse, 0))
				selected_animal._debug = True
				selected_animal.printDebug()
				draw_actors(Base_Surf, selected_animal)

		if (not is_paused):
			environment.update()
			draw_actors(Base_Surf, selected_animal)
			draw_boundary(Base_Surf)
			draw_stats(Base_Surf, font)
			fpsClock.tick(FPS)
			if (selected_animal is not None):
				selected_animal.printDebug()
			ticks += 1
		
		pygame.display.update()
		


if __name__ == '__main__':
	main()