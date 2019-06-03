"""
A Player class that you can configure to play the game.
"""

import logging
import time
import random
from copy import deepcopy

import numpy as np

from . import environments as env
from . import organisms as org

class Player:
    
    """
    Plays the game.
    """

    def __init__(self, n_herbivores, n_predators, tile, boardsize, turns, record_every=500):
        
        self.gameboard = env.Gameboard(boardsize=boardsize, tile=tile)
        self.turns = turns
        self.record_every = record_every
        
        for i in range(n_herbivores):
            a = org.Herbivore(location=(random.randint(boardsize[0]-1,boardsize[1]-1),
                                        random.randint(boardsize[0]-1,boardsize[1]-1)),
                              gameboard=self.gameboard)
            a.randomize_stats()
    
        for i in range(n_predators):
            a = org.Predator(location=(random.randint(boardsize[0]-1,boardsize[1]-1),
                                        random.randint(boardsize[0]-1,boardsize[1]-1)),
                              gameboard=self.gameboard)
            a.randomize_stats()
        
        self.initialize_recorder()
    
    def execute(self):
        """
        Run the game.
        """
        start = time.time()
        middle = time.time()
        initial_populations = self.populations_present()
        for i in range(0,self.turns+1):
            logging.info(f'---------- TURN {i} ----------')                
            if i%self.record_every == 0:
                self.recorder['alive'].append(self.get_creatures_on_board())
                self.recorder['dead'].append(self.get_removed_creatures())
                self.recorder['turn'].append(i)
                print(f'On turn {i}. nTime: {round(time.time()-middle,2)}')
                middle = time.time()
                if initial_populations != self.populations_alive():
                    print(f'!!!!! EXTINCTION !!!!!')
                    break
            self.gameboard.play()
        end = time.time()
        print(f'Simulation finished. Total time elapsed: {round(end-start,2)}')
            
        
    def initialize_recorder(self):
        self.recorder = {'alive':[], 'dead':[], 'turn':[]}
    
    def populations_present(self):
        """
        Returns a set of creature types that have ever been on the board
        """
        pop = {c.creature_type for c in self.all_creatures()} # set comprehension, not dictionary
        return pop
    
    def populations_alive(self):
        """
        Returns a set of creature types currently on the board
        """
        pop = {c.creature_type for c in self.get_creatures_on_board()} # set comprehension, not dictionary
        return pop
    
    def all_creatures(self):
        """
        Returns a list of all creatures living and dead that have been on the board
        """
        creatures = self.get_creatures_on_board()
        creatures.extend(self.get_removed_creatures())
        return creatures
    
    def get_creatures_on_board(self):
        """
        Returns a list of all currently living creatures
        """
        return self.gameboard.creatures.copy()
    
    def get_removed_creatures(self):
        """
        Returns a list of all creatures that have died so far
        """
        return self.gameboard.removed_creatures.copy()
    
    def get_populations(self):
        """
        Returns a dictionary where the keys are a type of creature (e.g., herbivore)
        and the values are lists all the creatures of that type on the board
        """
        pop = {cType:[] for cType in self.populations_present()}
        for creat in self.get_creatures_on_board():
            pop[creat.creature_type].append(creat)
                
        return pop
    