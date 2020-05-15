import pygame, sys
import random as rn
import math
import copy
from Game.settings import *


def get_board(size=9,probability=5):
    base = int(math.sqrt(size))
    side  = size

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (of valid base pattern)
    from random import sample
    def shuffle(s): return sample(s,len(s)) 
    rBase = range(base) 
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ] 
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    board = [ [nums[pattern(r,c)] for c in cols] for r in rows ]
    unsolved= copy.deepcopy(board)
    
    for i in range(len(unsolved)):
        for j in range(len(unsolved[0])):
            remove=rn.randint(0,10)>probability
            if(remove):
                unsolved[i][j]=0
    return board,unsolved


class Sudoku:
    def __init__(self):
        pygame.init()
        self.window=pygame.display.set_mode((WIDTH,HEIGHT))
        self.running = True
        print('loading board!!')
        self.solved,self.grid= get_board()
        self.grid[0][0]=self.solved[0][0]
        # self.grid=[
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        #     [0,0,0,0,0,0,0,0,0],
        # ]
        self.selected = None
        self.mouse_pos = None
        self.number=None
        self.state = "playing"
        self.finished=False
        self.lockedCells=[]
        self.incorrectCells=[]
        self.load()
        self.mistakes=0
        self.font = pygame.font.SysFont('arial',int(cell_size//2))

        print("done loading, let's play!")
    
    def load(self):
        for rIdx, row in enumerate(self.grid):
            for cIdx,col in enumerate(row):
                if(col!=0):
                    self.lockedCells.append([rIdx,cIdx])

    def run(self):
        while self.running:
            self.events(self.state)
            self.update(self.state)
            self.draw(self.state)
            if(self.finished):
                print('done yayy')
                break
        pygame.quit()
        sys.exit()

    def step(self):
        self.events(self.state)
        self.update(self.state)
        self.draw(self.state)

    def handleMouse(self):
        x_in_grid= grid_pos[0] <self.mouse_pos[0]< grid_pos[2]+grid_pos[0]
        y_in_grid= grid_pos[1] <self.mouse_pos[1]< grid_pos[3]+grid_pos[1]
        if( x_in_grid and y_in_grid):
            return ((self.mouse_pos[0]-grid_pos[0])//cell_size,(self.mouse_pos[1]-grid_pos[1])//cell_size)
        return False

    def events(self,state):
        if(state=='playing'):
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    self.running=False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected= self.handleMouse()
                    if(selected):
                        # print(selected)
                        self.selected=selected
                    else:
                        # print("not on board")
                        self.selected=None
                if event.type == pygame.KEYDOWN:
                    if(self.selected):
                        if('0'<event.unicode<='9'):
                            # self.grid[int(self.selected[0])][int(self.selected[1])]=int(event.unicode)
                            self.put_number(int(event.unicode),(int(self.selected[0]),int(self.selected[1])))
                    if(event.unicode==' '):
                        self.checkGame()
           
    def checkGame(self):
        self.incorrectCells=[]
        # for rIdx,row in enumerate(self.grid):
        #     for cIdx,col in enumerate(row):
        #         if(col!=0):
        #             if(col!=self.solved[rIdx][cIdx]):
        #                 self.incorrectCells.append([rIdx,cIdx])
        #                 self.mistakes+=1
        # self.checkRows()
        # self.checkCols()
        # self.checkSquares()
        self.checkAllValid()
        if(len(self.incorrectCells)==0):
            self.finished=self.allGameOver()
        self.selected=None     

    def valid(self, num, pos):
        #for The Ai
        if(not 0<num<10):
            return False

        #rows
        for i in range(ROWS):
            if(self.grid[pos[0]][i] == num and pos[1] !=i ):
                print('same row')
                return False
        
        #cols
        for i in range(COLS):
            if(self.grid[i][pos[1]] == num and pos[0] !=i):
                print('same col')
                return False
        
        #squares
        box_r = pos[1] // 3
        box_c = pos[0] // 3

        for i in range(box_c * 3, box_c* 3 + 3):
            for j in range(box_r*3, box_r*3+3):
                if(self.grid[i][j]== num and (i,j)!=pos):
                    print('same sqaure')
                    return False
        return True

    def checkAllValid(self):
        for i in range(ROWS):
            for j in range(COLS):
                if(self.grid[i][j]!=0 and [i,j] not in self.lockedCells):
                    if(not self.valid(self.grid[i][j], (i,j) )):
                        self.incorrectCells.append([i,j])
                        self.mistakes+=1

    def put_number(self,num,pos):
        self.grid[pos[0]][pos[1]]= num
        if(self.valid(num,pos)):
            # print("valid")
            return True
        else:
            # print("invalid")
            self.mistakes+=1
            self.incorrectCells.append(pos)
            return False

    def checkRows(self):
        for rIdx,row in enumerate(self.grid):
            possibles= [1,2,3,4,5,6,7,8,9]
            for cIdx in range(ROWS):
                if(self.grid[rIdx][cIdx] in possibles):
                    possibles.remove(self.grid[rIdx][cIdx])
                else:
                    if([rIdx,cIdx] not in self.lockedCells and self.grid[rIdx][cIdx]!=0 ):
                        self.incorrectCells.append([rIdx,cIdx])
                        self.mistakes+=1

    def checkCols(self):
        for cIdx in range(COLS):
            possibles= [1,2,3,4,5,6,7,8,9]
            for rIdx,row in enumerate(self.grid):
                if(self.grid[rIdx][cIdx] in possibles):
                    possibles.remove(self.grid[rIdx][cIdx])
                else:
                    if([rIdx,cIdx] not in self.lockedCells and self.grid[rIdx][cIdx]!=0 ):
                        self.incorrectCells.append([rIdx,cIdx])
                        self.mistakes+=1
    
    def checkSquares(self):
        for x in range(3):
            for y in range(3):
                possibles=[1,2,3,4,5,6,7,8,9]
                for i in range(3):
                    for j in range(3):
                        row= x*3+i
                        col= y*3+j
                        val=self.grid[row][col]
                        if val in possibles:
                            possibles.remove(val)
                        else:
                            if([row,col] not in self.lockedCells and self.grid[row][col]!=0 ):
                                self.incorrectCells.append([row,col])
                                self.mistakes+=1
                                
    def allGameOver(self):
        for rIdx,row in enumerate(self.grid):
            for cIdx,col in enumerate(row):
                if(col==0):
                    return False
        print('congrats you solved sudoku!!')
        return True
    
    def update(self,state):
        if(state=='playing'):
            self.mouse_pos= pygame.mouse.get_pos()

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

    def drawSelection(self,window,pos):
        margin = 3
        pygame.draw.rect(window,BLUE,(pos[0]*cell_size + grid_pos[0],pos[1]*cell_size+ grid_pos[1],cell_size+margin,cell_size+margin))

    def drawNumbers(self,window):
        margin = 10
        for rIdx,row in enumerate(self.grid):
            for cIdx,col in enumerate(row):
                if col != 0:
                    self.textToScreen(window,str(col),(rIdx*cell_size + grid_pos[0]+ margin,cIdx*cell_size+ grid_pos[1]+ margin))

    def textToScreen(self,window,text, pos, colour=BLACK):
        font = self.font.render(text,False,colour)
        window.blit(font,pos)

    def shadeLockedCells(self,window,lockedCells):
        margin=3
        for cell in lockedCells:
            pygame.draw.rect(window,GRAY,(cell[0]*cell_size + grid_pos[0],cell[1]*cell_size+ grid_pos[1],cell_size+margin,cell_size+margin))

    def shadeWrongCells(self,window,lockedCells):
        margin=3
        for cell in lockedCells:
            pygame.draw.rect(window,RED,(cell[0]*cell_size + grid_pos[0],cell[1]*cell_size+ grid_pos[1],cell_size+margin,cell_size+margin))

    def draw(self,state):
        if(state=='playing'):
            self.window.fill(WHITE)
             
            self.shadeWrongCells(self.window,self.incorrectCells)

            if self.selected:
                self.drawSelection(self.window,self.selected)


            self.shadeLockedCells(self.window,self.lockedCells)

            
            self.drawNumbers(self.window)
            
            self.drawGrid(self.window)

            self.textToScreen(self.window,f"Mistakes: {self.mistakes}", (450,40), colour=BLACK)

            pygame.display.update()

    def displayGrid(self):
        for row in self.grid:
            for col in row:
                print(f"{col}, ",end='')
            print()
