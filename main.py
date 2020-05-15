from Game.Sudoku import *
from Solvers.SimulatedAnnealing import *
from Solvers.GeneticAlgorithm import *

game= Sudoku()
agent= Gen(game)

agent.solve()
