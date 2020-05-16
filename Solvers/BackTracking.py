

class BckTrck:
    def __init__(self,sudoku):
        self.sudoku=sudoku
        self.board=sudoku.grid
        self.num_rows=len(self.board)
        self.num_cols=len(self.board[0])
        self.cur_row=0
        self.cur_col=0

    def solve(self):
        Done=100000
        self.sudoku.displayGrid()
        backTracking=False
        pos = self.get_next_pos(0,0)
        while Done>0:
            if(not pos):
                break
            print(pos)
            row,col= pos
            if([row,col] in self.sudoku.lockedCells):
                print('locked cells from pos')
                return

            curr_value = self.sudoku.grid[row][col]
            print('current: ',curr_value)
            self.sudoku.put_number(curr_value+1,(row,col))
            self.sudoku.checkGame()
            self.sudoku.step()
            if(self.sudoku.mistakes==0):
                print('changed with ',self.sudoku.grid[row][col])
                pos = self.get_next_pos(row,col)
            else:
                if(self.sudoku.grid[row][col]<9):
                    pos = pos
                else:
                    print('backtracking!')
                    self.sudoku.grid[row][col]=0
                    pos = self.get_prev_pos(row,col)
            self.sudoku.mistakes=0
            Done-=1
            
        print('you just solved sudoku!')
        self.sudoku.displayGrid()
        self.sudoku.checkGame()
        print(self.sudoku.mistakes)

    def get_next_pos(self,row,col):
        print('getting next slots for ',row,col)
        for r in range(row,self.num_rows):
            for c in range(col, self.num_cols):
                if(self.sudoku.grid[r][c]==0):
                    if((r,c) not in self.sudoku.lockedCells):
                        return (r,c)
            col=0
        print('no next slots')
        return None

    def get_prev_pos(self,row,col):
        print('getting prev for ',row,col)
        while row >=0:
            while col >=0:
                col-=1
                if([row,col] not in self.sudoku.lockedCells):
                    return (row,col)
            row-=1
            col=self.num_cols
        print('no previous slots')





