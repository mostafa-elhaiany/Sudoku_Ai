from Game.Sudoku import *
from Solvers.SimulatedAnnealing import *
from Solvers.GeneticAlgorithm import *
from Solvers.BackTracking import *
from Solvers.QLearning import *

game= Sudoku()
game.run()

# agent = QL(game) #QLearning
# agent=BckTrck(game) #backtracking
# agent = Gen(game) #GeneticAlgorithm
# agent = SimAnn(game) #simmulated Annealing

# agent.solve()