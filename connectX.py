import pygame
from pygame.locals import *

def get(x: int, y: int, TILE_SIZE, BORDER):
	i = x//TILE_SIZE
	j = y//TILE_SIZE
	if x%TILE_SIZE <= BORDER or x%TILE_SIZE>=TILE_SIZE-BORDER:
		return -1, -1
	if y%TILE_SIZE <= BORDER or x%TILE_SIZE>=TILE_SIZE-BORDER:
		return -1, -1
	return i, j
	
def clean(i: int, j: int, board):
	if i==-1 or board[0][i]!=0:
		return -1, -1
	j = 0
	while j<len(board) and board[j][i] == 0:
		j +=1
	return i, j-1
	
def mark(i, j, board, key):
	if i==-1:
		return board
	board[j][i] = key
	return board
	

	
def check_winner(board, key, W, H):
	def check(x1, y1, x2, y2, stepx, stepy):
		if x1 < 0 or x1 >= W or x2 < 0 or x2 >= W:
			return False
		if y1 < 0 or y1 >= H or y2 < 0 or y2 >= H:
			return False
		iter = 4
		while iter:
			if board[y1][x1]!=key:
				return False
			x1 += stepx
			y1 += stepy
			iter -= 1
		return True
	for x in range(W):
		for y in range(H):
			if check(x, y, x+3, y, 1, 0):
				return True
	for x in range(W):
		for y in range(H):
			if check(x, y, x, y+3, 0, 1):
				return True
	for x in range(W):
		for y in range(H):
			if check(x, y, x + 3, y + 3, 1, 1):
				return True
	for x in range(W):
		for y in range(H):
			if check(x, y, x - 3, y + 3, -1, 1):
				return True
	return False


def insert_text(info, string, x):
	if not pygame.font:
		return info
	
	font = pygame.font.Font(None, 24)
	text = font.render(string, 1, (0, 0, 0))
	info.blit(text, (3, x*26))
	return info
def main():
	TILE_SIZE = 80
	BORDER = 1
	W, H = 6, 7
	COLOR = [(0, 255, 0), (255, 0, 0)]
	name = ['GREEN', 'RED']
	
	pygame.init()
	screen = pygame.display.set_mode((W*TILE_SIZE + 300, H*TILE_SIZE))
	pygame.display.set_caption('ConnectX')
	background = pygame.Surface((W*TILE_SIZE, H*TILE_SIZE))
	background = background.convert()
	
	info  = pygame.Surface((300, H*TILE_SIZE))
	info = info.convert()
	info.fill((255, 255, 255))
	
	screen.blit(info, (W*TILE_SIZE, 0))
	pygame.display.flip()
	
	for i in range(W):
		for j in range(H):
			pygame.draw.rect(background, (255, 255, 255), (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE))
			pygame.draw.rect(background, (0, 0, 0), (i*TILE_SIZE, j*TILE_SIZE, BORDER, TILE_SIZE))
			pygame.draw.rect(background, (0, 0, 0), (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, BORDER))
			pygame.draw.rect(background, (0, 0, 0), ((i+1)*TILE_SIZE - BORDER, j*TILE_SIZE, BORDER, TILE_SIZE))
			pygame.draw.rect(background, (0, 0, 0), (i*TILE_SIZE, (j+1)*TILE_SIZE - BORDER, TILE_SIZE, BORDER))
	screen.blit(background, (0, 0))
	going = True
	turn = 0
	board = [[0 for i in range(W)] for j in range(H)]
	string = 'nothing to display'
	t = 1
	while going:
		for event in pygame.event.get():
			if event.type == QUIT:
				going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.unicode in ['q', 'Q']:
					going = False
			elif event.type == MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				i, j = get(x, y, TILE_SIZE, BORDER)	
				i, j = clean(i, j, board)
				board = mark(i, j, board, turn+1)
				if i==-1 and j==-1:
					continue
				if check_winner(board, turn+1, W, H):
					string = name[turn] + ' won the game '
					going = False
				pygame.draw.rect(background, COLOR[turn], (i*TILE_SIZE + BORDER, j*TILE_SIZE + BORDER, TILE_SIZE - 2*BORDER, TILE_SIZE - 2*BORDER))
				temp = 'turn:' + str(t) + '  color:' + name[turn] + '  column:' + str(i+1)
				info = insert_text(info, temp, t)
				if not going: info = insert_text(info, string, t+1)
				turn = 1 - turn
				t += 1
		#pygame.display.set_caption(name[turn])
		screen.blit(background, (0, 0))
		screen.blit(info, (W*TILE_SIZE, 0))
		pygame.display.flip()

	
	over = False
	while not over:
		
		#pygame.display.set_caption(string)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					over = True
				if event.unicode in ['q', 'Q']:
					over = True
			if event.type == QUIT:
				over = True
		screen.blit(background, (0, 0))
		pygame.display.flip()
	pygame.quit()


if __name__ == '__main__':
	main()