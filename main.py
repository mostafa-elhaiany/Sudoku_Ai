from Game.Sudoku import *
from Solvers.SimulatedAnnealing import *


game= Sudoku()
agent= SimAnn(game)

agent.solve()
