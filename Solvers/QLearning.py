import numpy as np
import copy, random
class QL:
    def __init__(self,sudoku):
        self.sudoku=sudoku
        self.empty_board = copy.deepcopy(self.sudoku.grid)
        self.num_rows=len(self.sudoku.grid)
        self.num_cols=len(self.sudoku.grid[0])
        self.observation_space_size = [self.num_rows,self.num_cols]
        self.action_space=10
        self.q_table=np.random.uniform(low=-2,high=0,size=(self.observation_space_size+[self.action_space]))
        self.initialize_table()
    
    def initialize_table(self):
        for pos in self.sudoku.lockedCells:
            action = self.sudoku.grid[pos[0]][pos[1]]
            self.q_table[pos] = [0 if i == action else -5 for i in range(self.action_space)] 

    def reset(self):
        self.sudoku.grid = copy.deepcopy(self.empty_board)
        self.sudoku.mistakes = 0
        return (0,0)

    def step(self,action):
        if([self.observation[0],self.observation[1]] not in self.sudoku.lockedCells):
            if(action==0):
                reward=-5
                done=False

            valid=self.sudoku.put_number(action,self.observation)
            if(valid):
                reward = 0
            else:
                reward = -2
            done = self.sudoku.checkGame()
            if done:
                reward = 1
        else:
           reward = -5
           done = False


        
        rows = self.observation[0]
        col = self.observation[1]

        rows+=1
        if(rows>=self.num_rows):
            col+=1
            rows=0
            if(col>=self.num_cols):
                rows=0
                col=0
        new_observation= (rows,col)

        self.sudoku.step()

        return new_observation, reward, done

    def solve(self):
        total_games=5000
    
        learning_rate=0.1
        discount = 0.95
        
        epsilon=0.5
        start_decay=1
        end_decay=total_games//2
        
        epsilon_decay_value=epsilon/(end_decay-start_decay)

        for episode in range(total_games):
            self.observation = self.reset()
            print(f"game number {episode}")
            done = False
            while not done:
                if(np.random.random()>epsilon):
                    action = np.argmax(self.q_table[self.observation])
                else:
                    action = random.randint(1,9)
                
                new_observation, reward, done = self.step(action)
               
                if not done:
                    max_future_q=np.max(self.q_table[new_observation])
                    current_q=self.q_table[self.observation+(action,)] 
                    
                    new_q = (1-learning_rate) * current_q + learning_rate*(reward + discount*max_future_q)
                    
                    self.q_table[self.observation+(action,)]=new_q

                elif(reward ==1 ):
                    self.q_table[self.observation+(action,)]=1
                    print("made it!!")

                self.observation = new_observation
            if(end_decay>=episode >=start_decay):
                epsilon-=epsilon_decay_value
        
        self.final_sol()
  
    def final_sol(self):
        self.reset()
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                action = np.argmax(q_table[(i,j)])
                valid=self.sudoku.put_number(action,(i,j))
        self.sudoku.displayGrid()
        print(self.sudoku.mistakes)


        


