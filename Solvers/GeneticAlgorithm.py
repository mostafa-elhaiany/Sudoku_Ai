import copy,random
from collections import deque

class Gen:
    def __init__(self,sudoku):
        self.sudoku=sudoku
        self.board=sudoku.grid
        self.num_rows=len(self.board)
        self.num_cols=len(self.board[0])
        self.population=500
        self.best_percentage=100
        self.best=[]
        self.score=0
        self.percentage= 1
        self.alpha=0.95
        self.start_decay= 90

    
    def solve(self):
        self.fillBoard()
        self.population_games=[]
        self.sudoku.checkGame()
        for _ in range(self.population//self.best_percentage):
            self.best.append([self.board,self.sudoku.mistakes])

        for _ in range(self.population):
            self.population_games.append(
                [copy.deepcopy(self.board),self.sudoku.mistakes]
            )

        print('num agents',len(self.population_games))
        print('taking best ',len(self.best))
        print('starting main loop')
        Done=1000
        self.start_decay = Done * (1-self.start_decay/100)
        while Done>0:
            self.randomize_boards() 
            
            self.get_scores()

            self.get_best()

            minScore=10000
            minIdx=-1
            for idx,item in enumerate(self.best):
                if(item[1]<minScore):
                    minScore=item[1]
                    minIdx=idx

            self.sudoku.grid=self.best[0][0]
            self.sudoku.checkGame()
            self.score=self.sudoku.mistakes
            self.sudoku.step()
            self.sudoku.mistakes=0

            Done-=1
            if(Done<self.start_decay):
                self.percentage*= self.alpha
            print(Done,":",self.score)
 


            

        self.sudoku.displayGrid()
        self.sudoku.checkGame()
        print(self.sudoku.mistakes)
    
    def fillBoard(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if(self.board[r][c]==0):
                    self.board[r][c]=random.randint(1,9)

    def randomize_boards(self):
        for i in range(self.population):
            for r in range(self.num_rows):
                for c in range(self.num_cols):
                    if([r,c] not in self.sudoku.lockedCells):
                        rand= random.random()
                        if(rand<self.percentage):
                            self.population_games[i][0][r][c]=random.randint(1,9)
    
    def get_scores(self):
        for i in range(self.population):
            self.sudoku.grid = copy.deepcopy(self.population_games[i][0])
            self.sudoku.checkGame()
            self.population_games[i][1]= self.sudoku.mistakes
            self.sudoku.mistakes=0

    def get_best(self):
        for i in range(self.population):
            cur = self.population_games[i]
            minScore=0
            minIdx=-1
            for idx,item in enumerate(self.best):
                if(item[1]>minScore):
                    minScore=item[1]
                    minIdx=idx
            if(minScore>cur[1]):
                self.best[minIdx]=cur


           
            
            
