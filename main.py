from Game.Sudoku import *
from Solvers.SimulatedAnnealing import *
from Solvers.GeneticAlgorithm import *
from Solvers.BackTracking import *
from Solvers.QLearning import *

game= Sudoku()
# game.run()
agent = QL(game)
agent.solve()