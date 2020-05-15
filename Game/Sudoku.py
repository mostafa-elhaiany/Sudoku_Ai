import pygame, sys
from settings import *



class Sudoku:
    def __init__(self):
        pygame.init()
        self.window=pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        self.grid= test_board

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()


    def events(self):
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                self.running=False
    
    def update(self):
        pass

    def drawGrid(self,window):
        pygame.draw.rect(window,BLACK,grid_pos,2)
        for r in range(ROWS):
            start_x=grid_pos[0]
            start_y= grid_pos[1]+(r*cell_size)
            end_x=grid_pos[0]+grid_pos[2]
            end_y= grid_pos[1]+(r*cell_size)
            if(r%3==0):
                thickness=4
            else:
                thickness=2
            pygame.draw.line(window, BLACK,(start_x,start_y),(end_x,end_y),thickness)
            for c in range(COLS):
                start_x=grid_pos[0]+(c*cell_size)
                start_y= grid_pos[1]
                end_x=grid_pos[0]+(c*cell_size)
                end_y= grid_pos[1]+grid_pos[3]
                if(c%3==0):
                    thickness=4
                else:
                    thickness=2
                pygame.draw.line(window, BLACK,(start_x,start_y),(end_x,end_y),thickness)            

    
    def draw(self):
        self.window.fill(WHITE)
        self.drawGrid(self.window)
        pygame.display.update()

