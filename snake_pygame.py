import pygame
from pygame.locals import *
import os
import random


def get_start():
	return 250, 250
	
def get_snake(snake: list, dir: str, food: tuple):
	head = snake[0]
	if dir == 'up':
		snake.insert(0, (head[0], head[1]-10))
	if dir == 'down':
		snake.insert(0, (head[0], head[1]+10))
	if dir == 'right':
		snake.insert(0, (head[0] + 10, head[1]))
	if dir == 'left':
		snake.insert(0, (head[0] - 10, head[1]))
	n = len(snake)
	if not food in snake: snake = snake[:n-1]
	return snake

def check(snake: list):
	head = snake[0]
	for i in range(1, len(snake)):
		if head == snake[i]:
			return True
	if head[0] < 0 or head[1] < 0 or head[1] > 500 or head[0] > 500:
		return True
	return False
def gen_food(snake: list):
	l = list()
	for i in range(1, 50):
		for j in range(1, 50):
			if (i*10, j*10) in snake:
				continue
			l.append((i*10, j*10))
	return random.choice(l)


def main():
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	#pygame.display.set_caption('snake apple')
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))
	
	screen.blit(background, (0, 0))
	pygame.display.flip()
	 
	x, y = get_start()
	snake = [(x, y), (x+10, y)]
	food = gen_food(snake)
	dir = 'up'
	prev_dir = 'up'
	vertical = ['up', 'down']
	horizontal = ['left', 'right']
	clock = pygame.time.Clock()
	length = 2
	going = True
	while going:
		#draw_snake(snake)
		clock.tick(15)
		pygame.display.set_caption(str(length))
		background.fill((250, 250, 250))
		for (x, y) in snake:
			pygame.draw.rect(background, (255, 0, 0), (x, y, 10, 10))
		
		#draw_food(food)
		pygame.draw.rect(background, (0, 255, 0), (food[0], food[1], 10, 10))
		for event in pygame.event.get():
			if event.type == QUIT:
				going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					going = False
				elif event.unicode == 'w' or event.key == K_UP:
					dir = 'up'
				elif event.unicode == 's' or event.key == K_DOWN:
					dir = 'down'
				elif event.unicode == 'a' or event.key == K_LEFT:
					dir = 'left'
				elif event.unicode == 'd' or event.key == K_RIGHT:
					dir = 'right'
		
		if dir in vertical and prev_dir in horizontal:
			prev_dir = dir
		if dir in horizontal and prev_dir in vertical:
			prev_dir = dir
		
		snake = get_snake(snake, prev_dir, food)
		if check(snake): going = False
		if food in snake: 
			food = gen_food(snake)
			length += 1
			#pygame.draw.rect(background, (0, 255, 0), (food[0], food[1], 10, 10))
		screen.blit(background, (0, 0))
		pygame.display.flip()
		
	game_over = pygame.Surface(screen.get_size())
	game_over = game_over.convert()
	game_over.fill((0, 0, 0))
	
	if pygame.font:
		font = pygame.font.Font(None, 36)
		text = font.render("Game Over : %s" %length, 1, (255, 255, 255))
		textpos = text.get_rect(centerx = game_over.get_width()/2)
		game_over.blit(text, textpos)
	
	screen.blit(game_over, (0, 0))
	pygame.display.flip()
	
	over = False
	while not over:
		for event in pygame.event.get():
			if event.type == QUIT:
				over = True
			elif event.type == KEYDOWN and event.unicode in ['q', 'Q']:
				over = True
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				over = True
	pygame.quit()

if __name__ == '__main__':
	main()