from Game.Sudoku import *
from Solvers.SimulatedAnnealing import *
from Solvers.GeneticAlgorithm import *
from Solvers.BackTracking import *
game= Sudoku()
# game.run()
agent= BckTrck(game)
agent.solve()
