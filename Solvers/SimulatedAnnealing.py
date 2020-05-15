import sys, random,math

class SimAnn:
    def __init__(self,sudoku):
        self.sudoku=sudoku
        self.board=sudoku.grid
        self.num_rows=len(self.board)
        self.num_cols=len(self.board[0])
        self.temprature=100000
        self.alpha=0.95
        self.prev = []

    
    def solve(self):
        self.fillBoard()

        self.sudoku.checkGame()
        self.score = self.sudoku.mistakes
        self.sudoku.mistakes=0
        i=4500
        while i>0 or self.score ==0:
            print(self.score)
            self.flip() 
            self.sudoku.checkGame()
            if self.score < self.sudoku.mistakes or self.boltzmann():
                self.revertAction()
            else:
                self.score=self.sudoku.mistakes

            self.temprature*= self.alpha

            self.sudoku.step()

            self.sudoku.mistakes=0

            i-=1
        self.sudoku.displayGrid()
        self.sudoku.checkGame()
        print(self.sudoku.mistakes)
        

    def fillBoard(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if(self.board[r][c]==0):
                    self.board[r][c]=random.randint(1,9)
    
    def flip(self):
        col= random.randint(0,self.num_cols-1)

        row1 =  random.randint(0,self.num_rows-1)

        row2 =  random.randint(0,self.num_cols-1)
        num_trials=0
        while([row1,col] in self.sudoku.lockedCells):
            row1 =  random.randint(0,self.num_rows-1)
            if(num_trials==10):
                num_trials=0
                col= random.randint(0,self.num_cols-1)
            num_trials+=1

        num_trials=0
        while([row2,col] in self.sudoku.lockedCells):
            row2 =  random.randint(0,self.num_rows-1)
            if(num_trials==10):
                num_trials=0
                col= random.randint(0,self.num_cols-1)
            num_trials+=1


        self.prev=[
            [ row1,col,self.board[row1][col] ],
            [ row2,col,self.board[row2][col] ],
            
        ]

        self.board[row1][col] = random.randint(1,9)
        self.board[row2][col] = random.randint(1,9)

    def boltzmann(self):
        r=random.random()
        try:
            return r < math.exp((self.sudoku.mistakes - self.score)/self.temprature)
        except:
            return True
    def revertAction(self):
        for action in self.prev:
            self.board[action[0]][action[1]] = action[2]
