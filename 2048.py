import pygame
from pygame.locals import *
import time
import random
class Grid(pygame.sprite.Sprite):
    def __init__(self, N, T):
        pygame.sprite.Sprite.__init__(self)
        self.mat = [[0 for i in range(N)] for j in range(N)]
        self.prev = [[0 for i in range(N)] for j in range(N)]
        self.n = N
        self.t = T
        self.empty = []
        self.add_random()
        self.add_random()

    def cal_random(self):
        temp = list()
        for i in range(self.n):
            for j in range(self.n):
                if self.mat[i][j] == 0:
                    temp.append((i, j))
        self.empty = temp

    def add_random(self):
        self.cal_random()
        l = len(self.empty)
        e = random.choice(self.empty)
        x, y = e
        self.empty = self.empty[:l-1]
        self.mat[x][y] = 2
        return

    def rotate_clockwise(self, mat):
        temp = [[ 0 for i in range(self.n)] for j in range(self.n)]
        n = self.n
        a = 0
        b = 0
        for i in range(n):
            for j in range(n-1, -1, -1):
                temp[a][b] = mat[j][i]
                b += 1
                if b == n:
                    b = 0
                    a += 1
        return temp

    def rotate_anticw(self, mat):
        temp = [[ 0 for i in range(self.n)] for j in range(self.n)]
        n = self.n
        a = 0
        b = 0
        for i in range(n-1, -1, -1):
            for j in range(n):
                temp[a][b] = mat[j][i]
                b += 1
                if b == n:
                    b = 0
                    a += 1
        return temp
        
    def move(self, mat):
        n = self.n
        for i in range(n):
            for r in range(n-2, -1, -1):
                for c in range(n):
                    if mat[r][c] == 0 and mat[r+1][c] != 0:
                        mat[r][c] = mat[r+1][c]
                        mat[r+1][c] = 0
        return mat
    def add1(self, mat):
        n= self.n
        for r in range(n-1):
            for c in range(n):
                if mat[r][c] == mat[r+1][c]:
                    mat[r][c] = 2 * mat[r][c]
                    mat[r+1][c] = 0
        return mat

    def moveup(self):
        temp = self.mat
        temp = self.move(temp)
        temp = self.add1(temp)
        temp = self.move(temp)
        self.mat = temp

    def movedown(self):
        temp = self.mat
        temp = self.rotate_clockwise(temp)
        temp = self.rotate_clockwise(temp)
        temp = self.move(temp)
        temp = self.add1(temp)
        temp = self.move(temp)
        temp = self.rotate_anticw(temp)
        temp = self.rotate_anticw(temp)
        self.mat = temp
    def moveleft(self):
        temp = self.mat
        temp = self.rotate_clockwise(temp)
        temp = self.move(temp)
        temp = self.add1(temp)
        temp = self.move(temp)
        temp = self.rotate_anticw(temp)
        self.mat = temp
    def moveright(self):
        temp = self.mat
        temp = self.rotate_anticw(temp)
        temp = self.move(temp)
        temp = self.add1(temp)
        temp = self.move(temp)
        temp = self.rotate_clockwise(temp)
        self.mat = temp

    def p(self, mat):
        for i in range(self.n):
            for j in range(self.n):
                print(mat[i][j], end = ' ')
            print()
        print("**")

    def prepare(self, x):
        if x == 0:
            x = ''
        else:
            x = str(x)
        s = pygame.Surface((self.t, self.t))
        s.fill((255, 255, 255))
        font = pygame.font.SysFont('Arial', 16)
        text = font.render(x, True, (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = self.t//2, self.t//2
        s.blit(text, text_rect)
        return s
        
    def update(self, screen):
        if not self.same():
            #print('new_move')
            self.add_random()

        for i in range(self.n):
            for j in range(self.n):
                self.prev[i][j] = self.mat[i][j]
        
        n = self.n
        for i in range(n):
            for j in range(n):
                print(self.mat[i][j], end = ' ')
            print()
        print('************')

        for i in range(n):
            for j in range(n):
                if self.mat[i][j] == 0:
                    continue
                s = self.prepare(self.mat[i][j])
                screen.blit(s, (j*self.t, i*self.t))
                
        return screen
    def won(self):
        n = self.n
        for i in range(n):
            for j in range(n):
                if self.mat[i][j] == 2048:
                    return True
        return False

    def filled(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.mat[i][j] == 0:
                    return False
        return True

    def same(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.mat[i][j] != self.prev[i][j]:
                    return False
        return True
    def lost(self):
        if self.filled() and self.same():
            return True
        else:
            return False
        
if __name__=='__main__':

    #constants
    TILE_SIZE = 80
    BORDER = 1
    N, N = 4, 4
    W, H = N*TILE_SIZE, N*TILE_SIZE
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption('2048')
    background = pygame.Surface(screen.get_size())
    background.fill((200, 200, 200))
    background = background.convert()

    screen.blit(background, (0, 0))
    pygame.display.flip()

    grid = Grid(N, TILE_SIZE)

    playing = True
    wrong = False
    while playing:
        event = pygame.event.wait()
        wrong = False
        if event.type == QUIT:
            playing = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE or event.unicode in ['q', 'Q']:
                playing = False
            elif event.unicode in ['w', 'W']:
                grid.moveup()
            elif event.unicode in ['s', 'S']:
                grid.movedown()
            elif event.unicode in ['a', 'A']:
                grid.moveleft()
            elif event.unicode in ['d', 'D']:
                grid.moveright()
            else:
                wrong = True
        else:
            wrong = True
        if not wrong:
            if grid.lost():
                pygame.display.set_caption('LOST')
                playing = False
            if grid.won():
                pygame.display.set_caption('WON')
                playing = False
            background.fill((200, 200, 200))
            background = grid.update(background)
            screen.blit(background, (0, 0))
            pygame.display.flip()
            wrong = False
    time.sleep(100)
    pygame.quit()
    
            
