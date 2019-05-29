"""
A Player class that you can configure to play the game.
"""

import logging
import time
import random

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
    
        for i in range(n_predators):
            pass
        
        self.initialize_statistics_dictionary()
    
    def execute(self):
        """
        Run the game.
        """
        start = time.time()
        middle = time.time()
        for i in range(0,self.turns+1):
            logging.info(f'---------- TURN {i} ----------')
            if i%self.record_every == 0:
                self.record_statistics(i)
                print(f'On turn {i}. nTime: {round(time.time()-middle,2)}')
                middle = time.time()
            self.gameboard.play()
        end = time.time()
        print(f'Simulation finished. Total time elapsed: {round(end-start,2)}')
            
    def initialize_statistics_dictionary(self):
        empty_statdict = {cType:[] for cType in self.populations_present()}
        subdict = {'maxenergy':[],
                   'maxvitality':[],
                   'speed':[],
                   'efficiency':[],
                   'fertility':[],
                   'attack_power':[],
                   'defense':[],
                   'alive':[]}
        
        for cType in empty_statdict:
            empty_statdict[cType] = subdict
            
        empty_statdict['turn'] = []
        self.statdict = empty_statdict
            
    def populations_present(self):
        pop = {c.type for c in self.all_creatures()} # set comprehension, not dictionary
        return pop
    
    def record_statistics(self, turn):
        populations = self.get_populations()
        for key,val in self.statdict.items():
            if key == 'turn':
                val.append(turn)
            else:
                population = populations[key]
                val['maxenergy'].append(self.population_mean_maxenergy(population))
                val['maxvitality'].append(self.population_mean_maxvitality(population))
                val['speed'].append(self.population_mean_speed(population))
                val['efficiency'].append(self.population_mean_efficiency(population))
                val['fertility'].append(self.population_mean_fertility(population))
                val['attack_power'].append(self.population_mean_attack_power(population))
                val['defense'].append(self.population_mean_defense(population))
                val['alive'].append(len(population))
    
    def all_creatures(self):
        creatures = self.get_creatures_on_board()
        creatures.extend(self.get_removed_creatures())
        return creatures
    
    def get_creatures_on_board(self):
        return self.gameboard.creatures
    
    def get_removed_creatures(self):
        return self.gameboard.removed_creatures
    
    def get_alive_creatures(self):
        return [c for c in self.get_creatures_on_board() if c.is_alive]
    
    def get_populations(self):
        pop = {cType:[] for cType in self.populations_present()}
        for creat in self.get_alive_creatures():
            pop[creat.type].append(creat)
                
        return pop
    
    def population_mean_maxenergy(self, creatures):
        return np.mean([c.maxenergy for c in creatures])
    
    def population_mean_maxvitality(self, creatures):
        return np.mean([c.maxvitality for c in creatures])
    
    def population_mean_speed(self, creatures):
        return np.mean([c.speed for c in creatures])
    
    def population_mean_efficiency(self, creatures):
        return np.mean([c.efficiency for c in creatures])
    
    def population_mean_fertility(self, creatures):
        return np.mean([c.fertility for c in creatures])
    
    def population_mean_attack_power(self, creatures):
        return np.mean([c.attack_power for c in creatures])
    
    def population_mean_defense(self, creatures):
        return np.mean([c.defense for c in creatures])
    
    