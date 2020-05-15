from Game.Sudoku import *
from Solvers.SimulatedAnnealing import *
from Solvers.GeneticAlgorithm import *
from Solvers.BackTracking import *
game= Sudoku()
agent= BckTrck(game)

agent.solve()
