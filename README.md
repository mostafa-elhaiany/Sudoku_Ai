# Sudoku Ai

multiple Agents that solve the game soduku

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

The code runs on python3
you'll need the following libraries

```
pygame
```
which handles the game GUI

and 

```
numpy
```
which was used in Qlearning for building the qtable

### Installing



make sure you have a python3 setup up and running

then to install the needed libraries

```
pip install pygame numpy
```

to make sure everything is up and running
```
python main.py
```
this should start the game of sudoku where you can play it yourself 


### Break down into file system and Algorithms used

the code is divided into two parts, the game, and the solvers

```
GAME
```
for the game folder settings hold some of the constants and settings used for colours number of rows and columns etc,
Sudoku holds the code for building the game with pygame GUI, all the needed information are commented in the file

```
Solvers
```
for the solvers folder there is a different class for every solver,

1)  BackTracking.py
        backtracking is an algorithm where we try every possible combination of numbers for a given cell and we find one that works and then we move on to the next cell, it may seem as a naive brute force approach but the backtracking comes in when there is a cell with no possible solution then we backtrack to the previous cell and try a different solution for that one, and we either find another solution and keep going or we have to backtrack further

        the idea is we're only moving forward with solutions that work at every given time step
        and by reaching the end we're sure that we've solved the current soduku puzzle

2)  GeneticAlgorithm.py
        genetic algorithms are in a way a "survival of the fittest" algorithm,
        you take a population of n genomes and each genome has a randomly filled board,
        you calculate their fittness which is a measure of how good/bad the genome is,
        you then take the best m genomes out of the whole population and you breed them,
        for every genome in the best one there is a mutation rate, and a crossover rate.
        mutation rate is a measure of how likely it is for each genome to mutate,
        meaning getting a new random value that wasn't in the genepool to begin with.
        Crossover rate is the rate at which 2 genomes can form a new genome, where we take
        some valeus from the first one and some values from the other,
        and finally there is a chance where the genome can go on to the next population unchanged

        rinse and repeat for a few populations you end up with a good population able to solve the given puzzle
        with enough tuning and time

3)  SimulatedAnnealing.py
        SimulatedAnnealing is an algorithm where you don't always have to improve, sometimes you have to explore
        you take steps further and closer as you go to find the optimal solution.
        
        the idea is mainly how you'd play a game where you're not sure how you're supposed to reach the end goal
        you'll play randomly, maybe score a few points, and as you score more and more, or take further steps into the game
        you'll start playing with more focus not as random as you were in the beginning as not to lose points
        the algorithm starts by choosing a column and two rows, and then it randomly adds a value

        now there is 2 scenarios that might occure, 1 the new score is worse than the old one
        in this case the changes we made is probably not a good one so we revert back

        the other scenario is that the change is actually a better one, so you'd wanna keep that, however,
        there is the Boltzmann distribution notion where you wanna revert back in case you're in a certain probability
        and this is handled mostly by the Temprature

        in the beginning the temprature is hot, or a large value, meaning you're more susceptible to change your values
        then in time the temprature decays into colder smaller values meaning you're less likely to change numbers you've already added.

        and in time the algorithm seams to solve the problem

4)  QLearning.py
        Qlearning is a smart algorithm that builds a table where given a certain observation you can get the best action you can do in that certain situation.

        let's assume you're in a maze, an observation we can use would be the location, and the reward we get could be how far we are from the goal, so the goal would be to minimize that function, so at first you take random actions
        and based on the rewards you get on each action, you learn whether that was a good or a bad move

        I've used the same notion here,so the idea was to give the table as an observation the entire board, however, that uses too much memory and I believe isn't needed.
        so I decided to try the observation as the cell you're in(row and column value)
        and the idea is to train the model given a cell it'll know which value should be plugged in that cell

        and it loops over all the cells over and over till it gets it right, so adding a right value is rewarded by 0 adding a wrong value is rewarded by -2 and winning the game is rewarded by 1 

        however this is quite slow, I believe adding rewards based on if the number in that cell is right for the row but not the column perhaps so it knows it needs to be unique in the row, and then for the column as well

        moreover we can change the observation states to hold more info rather than just the cell you're in




### Running the Agents

in the main file game is the sudoku puzzle that the Ai will try to solve,
comment the game.run() function and uncomment which agent you need to solve the game along with the agent.solve() function






