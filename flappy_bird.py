import pygame
import random
from pygame.locals import *

def main():

	W, H = 600, 500
	DIST_COLS = 150
	SPEED = 5
	COL_WIDTH = 30
	POS = H//2
	BW, BH = 15, 15
	GRAVITY = 4
	JUMP = 25
	POS_X = 30
	
	pygame.init()
	screen = pygame.display.set_mode((W, H))
	
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((255, 255, 255))
	
	screen.blit(background, (0, 0))
	pygame.display.flip()
	
	dist = DIST_COLS
	clock = pygame.time.Clock()
	
	a = []
	b = []
	
	going = True
	
	score = 0
	pos = POS
	while going:
		clock.tick(10)
		background.fill((255, 255, 255))
		temp_a = []
		temp_b = []
		for [x, y] in a:
			x -= SPEED
			if x + COL_WIDTH < POS_X and x + COL_WIDTH + SPEED >= POS_X:
				score += 1
			if x + COL_WIDTH > 0:
				temp_a.append([x, y])
		for [x, y] in b:
			x -= SPEED
			if x + COL_WIDTH < POS_X and x + COL_WIDTH + SPEED >= POS_X:
				score += 1
			if x + COL_WIDTH > 0:
				temp_b.append([x, y])
		a = temp_a
		b = temp_b
		dist += SPEED
		
		if dist >= DIST_COLS:
			x, y = W, random.randint(200, 290)
			t = [x, y]
			if random.random() < 0.5:
				a.append(t)
			else:
				b.append(t)
			dist = 0
		pos += GRAVITY
		for event in pygame.event.get():
			if event.type == KEYDOWN and (event.key == K_UP or event.unicode in ['w', 'W']):
				pos -= JUMP 
			if event.type == QUIT:
				going = False
			elif event.type == KEYDOWN and event.unicode in ['q', 'Q']:
				going = False
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				going = False
		
		if pos>=H or pos <=0:
			going = False
		
		#from bottom to up
		r1 = pygame.Rect(POS_X, pos, BW, BH)
		for (x, y) in b:
			r2 = pygame.Rect(x, 0, COL_WIDTH, y)
			if r1.colliderect(r2):
				going = False
		for (x, y) in a:
			r2 = pygame.Rect(x, H-y, COL_WIDTH, y)
			if r1.colliderect(r2):
				going = False
		
		
		pygame.draw.rect(background, (255, 0, 0), (POS_X, pos, BW, BH)) 
		for (x, y) in a:
			pygame.draw.rect(background, (0, 255, 0), (x, H - y, COL_WIDTH, y))
		
		for (x, y) in b:
			pygame.draw.rect(background, (0, 255, 0), (x, 0, COL_WIDTH, y))
		pygame.display.set_caption(str(score))
		screen.blit(background, (0, 0))
		pygame.display.flip()
	quit = False
	while not quit:
		screen.blit(background, (0, 0))
		pygame.display.set_caption('Game Over :' + str(score))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == QUIT:
				quit = True
			if event.type == KEYDOWN:
				if event.unicode in ['q', 'Q']:
					quit = True
				if event.key == K_ESCAPE:
					quit = True
	
	pygame.quit()
	
if __name__ == '__main__':
	main()