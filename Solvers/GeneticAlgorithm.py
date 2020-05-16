import copy,random
from collections import deque


class Genome:
    def __init__(self, board, score):
        self.board=copy.deepcopy(board)
        self.fitness=score
    
    def compare_to(self,genome):
        return self.fitness - genome.fitness

    def mutate(self,lockedCells):
        
        new_board = copy.deepcopy(self.board)

        num_rows = random.randint(1,10)
        num_cols= random.randint(1,10)

        for rows in range(num_rows):
            for cols in range(num_cols):
                r=random.randint(0,len(new_board)-1)
                c=random.randint(0,len(new_board[r])-1)
                while([r,c] in lockedCells):
                    r=random.randint(0,len(new_board)-1)
                    c=random.randint(0,len(new_board[r])-1)
                old_cell = new_board[r][c]
                new_cell=old_cell
                while(new_cell==old_cell):
                    new_board[r][c]= random.randint(1,9)
                    new_cell = new_board[r][c]
                    
        return new_board

    def crossover(self, genome):
        new_board = copy.deepcopy(self.board)

        for r in range(len(new_board)):
            for c in range(len(new_board[r])):
                percentage = random.random()
                if percentage > 0.5:
                    new_board[r][c] = genome.board[r][c]

        return new_board


class Gen:
    def __init__(self,sudoku):
        self.sudoku=sudoku
        self.board=sudoku.grid
        self.num_rows=len(self.board)
        self.num_cols=len(self.board[0])
        self.population=3000
        self.num_best_genomes=30
        self.best=[]
        self.genomes=[]
        self.score=0
        self.percentage= 1
        self.alpha=0.95
        self.start_decay= 90
        self.mutate_percentage=0.75
        self.crossover_percentage = 0.5
        self.initialize()
    
    def initialize(self):
        self.empty_board=copy.deepcopy(self.board)

        for _ in range(self.population):
            self.fillBoard()
            genome_board=copy.deepcopy(self.board)
            self.sudoku.grid = copy.deepcopy(genome_board)
            self.sudoku.checkGame()
            self.genomes.append(
                Genome(genome_board,self.sudoku.mistakes)
            )
            self.sudoku.mistakes=0
            self.sudoku.grid=copy.deepcopy(self.board)
            self.board=copy.deepcopy(self.empty_board)



        for i in range(self.num_best_genomes):
            min_fitness = 100
            min_index= -1
            prev_index=[]
            for idx in range(self.population):
                if(self.genomes[idx].fitness<min_fitness and idx not in prev_index):
                    min_fitness=self.genomes[idx].fitness
                    min_index = idx
            if(min_index!=-1):
                self.best.append(self.genomes[min_index])
                prev_index.append(min_index)


            self.board = copy.deepcopy(self.best[0].board)
            self.score = self.best[0].fitness

    def solve(self):
        print('num agents',len(self.genomes))
        print('taking best ',len(self.best))
        print('starting main loop')
        Done=100
        while Done>0:
            self.repopulate()

            self.get_best()

            self.sudoku.grid=copy.deepcopy(self.board)
            self.sudoku.mistakes=0
            self.sudoku.checkGame()
            self.score=self.sudoku.mistakes
            self.sudoku.step()
            self.sudoku.mistakes=0
            print('score: ',self.score)


            Done-=1
 
        self.sudoku.displayGrid()
        self.sudoku.checkGame()
        print(self.sudoku.mistakes)
            
    def fillBoard(self):
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if(self.board[r][c]==0):
                    self.board[r][c]=random.randint(1,9)

    def repopulate(self):
        self.genomes=[]

        for _ in range(self.population):
            first_genome = random.randint(0,len(self.best)-1)
            second_genome = first_genome
            while second_genome != first_genome:
                second_genome = random.randint(0,len(self.best)-1)
            
            percentage = random.random()

            if(percentage<=self.mutate_percentage):
                new_board = self.best[first_genome].mutate(self.sudoku.lockedCells)
                self.sudoku.mistakes=0
                self.sudoku.grid = copy.deepcopy(new_board)
                self.sudoku.checkGame()
                self.genomes.append(
                    Genome(new_board, self.sudoku.mistakes)
                )
            else:
                percentage2=random.random()
                if(percentage2<=self.crossover_percentage):
                    new_board = self.best[first_genome].crossover(self.best[second_genome])
                    self.sudoku.mistakes=0
                    self.sudoku.grid = copy.deepcopy(new_board)
                    self.sudoku.checkGame()
                    self.genomes.append(
                        Genome(new_board, self.sudoku.mistakes)
                    )
                else:
                    self.genomes.append(
                        self.best[first_genome]
                    )
            

        while(len(self.genomes)>self.population):
            choice = random.randint(0,len(self.genomes)-1)
            self.genomes.remove(self.genomes[choice])

            
        
        # self.checkDifferent()


        # print('===============')
        # for i in range(self.population):
        #     print(self.genomes[i].fitness, end=" ")
        # print('\n===============')
   
    def checkDifferent(self):
        for i in range(1,self.num_best_genomes):
            if(self.best[i-1].board==self.best[i].board):
                print('same boardddd!!!!!!!!!!!!!')
            else:
                print("dfff board!!!!!!!!!!!!!!")

    def get_best(self):
        # self.best=[]
        for i in range(self.num_best_genomes):
            min_fitness = 100
            min_index= -1
            prev_index=[]
            for idx in range(self.population):
                if(self.genomes[idx].fitness<min_fitness and idx not in prev_index):
                    min_fitness=self.genomes[idx].fitness
                    min_index = idx
            if(min_index!=-1):
                min_best_index= self.get_min_best()
                if(self.best[min_best_index].fitness > min_fitness):
                    self.best[min_best_index] = self.genomes[min_index]
                    
                prev_index.append(min_index)

            best_idx=self.get_max_best()
            self.board = copy.deepcopy(self.best[best_idx].board)
            # print(f'score changed from {self.score} to {self.best[best_idx].fitness}')
            self.score = self.best[best_idx].fitness

    def get_min_best(self):
            max_fitness = 0
            min_index= -1
            prev_index=[]
            for idx in range(len(self.best)):
                if(self.best[idx].fitness>max_fitness and idx not in prev_index):
                    max_fitness=self.best[idx].fitness
                    min_index = idx
            return idx

    def get_max_best(self):
        min_fitness = 100
        min_index= -1
        prev_index=[]
        for idx in range(len(self.best)):
            if(self.best[idx].fitness<min_fitness and idx not in prev_index):
                min_fitness=self.best[idx].fitness
                min_index = idx
        return idx
            
            
