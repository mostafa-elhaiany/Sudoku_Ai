

class BckTrck:
   def __init__(self,sudoku):
        self.sudoku=sudoku
        self.board=sudoku.grid
        self.num_rows=len(self.board)
        self.num_cols=len(self.board[0])
        self.cur_row=0
        self.cur_col=0

   def solve(self):
        Done=10000
        self.sudoku.displayGrid()
        while Done>0:
            print(self.cur_row,self.cur_col)
            self.sudoku.step()
            if([self.cur_row,self.cur_col] in self.sudoku.lockedCells):
                print('locked cell')
                self.cur_row+=1
                if(self.cur_row ==9 ):
                    self.cur_col+=1
                    self.cur_row=0
                    if(self.cur_col==9):
                        print('you have just solved soduku')
                        self.sudoku.displayGrid()
                        return
                continue
            
            while(True):
                if(self.sudoku.grid[self.cur_row][self.cur_col]<9):
                    self.sudoku.grid[self.cur_row][self.cur_col]+=1
                
                self.sudoku.checkGame()
                self.sudoku.step()
                if self.sudoku.mistakes == 0:
                    self.cur_row+=1
                    if(self.cur_row == 9):
                        self.cur_col+=1
                        self.cur_row=0
                        if(self.cur_col==9):
                            print('you have just solved soduku')
                            self.sudoku.displayGrid()
                            return
                        break
                else:
                    if(self.sudoku.grid[self.cur_row][self.cur_col] == 9):
                        self.sudoku.grid[self.cur_row][self.cur_col] = 0
                        self.cur_row-=1
                        if(self.cur_row<0):
                            self.cur_row=0
                            self.cur_col-=1
                            if(self.cur_col<0):
                                print('something is terribly wrong')
                                return
                    else:
                        break


            self.sudoku.mistakes=0
            # print('score: ',self.score)
            Done-=1
 
        self.sudoku.displayGrid()
        self.sudoku.checkGame()
        print(self.sudoku.mistakes)


    
        