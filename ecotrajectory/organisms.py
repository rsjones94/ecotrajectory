"""
Various kinds of organisms for use in the simulation.
"""

import itertools
import math
import random

import numpy as np

def angle_between_points(ptA, ptB):
    """
    Get the angle in radians between the x-axis and the vector connecting
    ptA and ptB
    
    Vectors in quadrants 1 and 2 have positive angles
    Vectors in quadrants 3 and 4 have negative angles
    """
    
    delta_x = ptB[0] - ptA[0]
    delta_y = ptB[1] - ptA[1]
    return math.atan2(delta_y, delta_x)

def angle_diff(a1, a2):
    """
    Get the smallest absolute difference between two angles, taking into account
    that angle_between_points returns negative angles for vectors in quads 3 and 4
    """
    
    a = a2 - a1
    if a > np.pi:
        a -= 2*np.pi 
    elif a < -np.pi:
        a += 2*np.pi 
    
    return abs(a)

def get_directions():
    """
    Get the 8 possible directions
    """

    change_vals = [1,0,-1]
    possible_directions = [l for l in
                           itertools.product(change_vals, repeat=2)]
    possible_directions.remove((0,0))
    return possible_directions

class Creature():
    
    MOVEMENT_COST = -10
    ATTACK_COST = -5
    MATING_COST = -25
    
    PERFECT_STATS = [200, 100, 50, .8, .8, 3, 1]
    
    """
    An animal-esque creater to be placed on a Gameboard.
    
    Attributes:
        energy(float): the energy the creature has for tasks
        speed(int): the number of movements a creature gets per turn
        efficiency(float): energy costs will multiplied by 1-efficiency
        vitality(float): the health of the creature
        attack_power(float): the power of the creature's attacks
        defense(float): the fraction of an attack against the creature that
            will be disregarded
        fertility(float): the liklihood of a creature successfully breeding
        aggression(float): the liklihood a creature will engage in conflict
        location(tuple of int): the location of the creature on the board
        gameboard(Gameboard): a Gameboard object that the creature will reside on
        is_alive(bool): self explanatory
        MOVEMENT_COST(float): cost to move
        ATTACK_COST(float): cost to attack
        MATING_COST(float): cost to mate
        PERFECT_STATS(list of float): a list of ideal scores for the attributes
            returned by power_stats
    """
    
    def __init__(self, location, gameboard, maxenergy=100, speed=1, efficiency=0,
                 maxvitality=100, attack_power=10, defense=0.5, fertility=0.8,
                 aggression=0.25):
        
        self.energy = maxenergy/2
        self.speed = speed
        self.efficiency = efficiency
        self.vitality = maxvitality
        self.attack_power = attack_power
        self.defense = defense
        self.fertility = fertility
        self.aggression = aggression
        
        self.gameboard = gameboard
        self.location = location
        
        # creatures start with half energy and full vitality
        self.maxenergy = maxenergy
        self.maxvitality = maxvitality
        self.is_alive = True
        
    def move(self, delX, delY):
        """
        Moves the creature on the board.
        """
        new_pos = (self.location[0]+delX, self.location[1]+delY)
        if self.gameboard.pos_is_valid(new_pos):
            self.location = new_pos
            self.change_energy(self.MOVEMENT_COST)
        else:
            raise IndexError(f'Creature cannot move to {new_pos}')
            
    def move_randomly(self):
        
        directions = get_directions()
        length = len(directions)
        for i in range(length):
            try:
                direction = random.choice(directions)
                self.move(direction[0], direction[1])
                return None
            except IndexError:
                directions.remove(direction)
        
        raise IndexError('No valid movements found')
            
    def get_closest_direction(self, loc):
        """
        Find the direction that is the closest to pointing right at a target
        location.
        
        Returns a tuple of form (x,y) where x and y are -1, 0 or 1
        """
        target_angle = self.direction_to_location(loc)
        
        possible_directions = get_directions()
        
        angles = [angle_diff(angle_between_points((0,0),l),target_angle) 
                  for l in possible_directions]
        
        return possible_directions[np.argmin(angles)]
            
    def move_toward(self, loc):
        """
        Move the creature toward a target location, loc (x,y)
        """
        
        win_direction = self.get_closest_direction(loc)
        self.move(win_direction[0], win_direction[1])
        
    def die(self):
        
        self.is_alive = False
        
    def get_current_tile(self):
        
        return self.gameboard.landscape[self.location[0],
                                        self.location[1]]
        
    def attack(self, target):
        """
        Give the target (a Creature object) a whack.
        """
        target.take_damage(self.attack_power)
        self.change_energy(self.ATTACK_COST)
        
    def change_energy(self, amount):
        
        self.energy += amount*(1-self.efficiency)
        if self.energy > self.maxenergy:
            self.energy = self.maxenergy
        elif self.energy <= 0:
            self.die()
            
    def change_vitality(self, amount):
        
        self.vitality += amount
        if self.vitality > self.maxvitality:
            self.vitality = self.maxvitality
        elif self.vitality <= 0:
            self.die()
            
    def take_damage(self, amount):
        
        self.change_vitality(-amount*(1-self.defense))
        
    def mating_stats(self):
        """
        Returns a list of stats that can are used for mating
        """
        
        stats = self.power_stats()
        stats.append('aggression')
        
        return stats
        
    def power_stats(self):
        """
        Returns a list of attributes relevant to calculating power scores
        """
        
        return ['maxenergy', 'maxvitality', 'attack_power', 'defense',
                'efficiency', 'speed', 'fertility']
        
    def get_vals(self, atts):
        """
        Takes a list of attributes and returns the values for them
        """
        
        return [getattr(self,l) for l in atts]
        
    def power_score(self):
        """
        Generate a score that assesses the overall power of a creature.
        Normalizes Creature attributes against "perfect attributes" and then
        sums the scores.
        
        Returns:
            A tuple of two numbers. The first is the absolute power score.
            The second is the relative power score (ratio of absolute score to
            a perfect score). A 1 is a "perfect" score but not the max.
        """
        
        scores = [actual/perfect for actual,perfect in
                  zip(self.get_vals(self.power_stats()),self.PERFECT_STATS)]
        
        power_score = sum(scores)
            
        return power_score, power_score/len(scores)
    
    def direction_to_location(self, loc):
        """
        Get the angle in radians between the x-axis and the vector connecting
        the current location to another location, loc (x,y)
        
        Vectors in quadrants 1 and 2 have positive angles
        Vectors in quadrants 3 and 4 have negative angles
        """
        
        return angle_between_points(self.location, loc)
    
    def mate(self, target, allowMutation=False):
        """
        Create an offspring with another Creature
        """
        
        own_vals = self.get_vals(self.mating_stats())
        target_vals = target.get_vals(target.mating_stats())
        offspring_vals = [(o+t)/2 for o,t in zip(own_vals,target_vals)]

        val_dict = {stat:val for stat,val in zip(self.mating_stats(),offspring_vals)}
    
class Herbivore(Creature):
    
    feed_amount = 10
    
    """
    They just like eatin' plants.
    
    Attributes:
        feed_amount(float): the amount of plant material/energy that can be
            converted in a single feeding
    """
    
    def __init__(self, location, gameboard):
        super(Herbivore, self).__init__(location=location,
                                        gameboard=gameboard,
                                        maxenergy=100,
                                        speed=1,
                                        efficiency=0,
                                        maxvitality=100,
                                        attack_power=0,
                                        defense=0.5,
                                        fertility=0.8,
                                        aggression=0.0)
    
    def graze(self):
        """
        Munch some plants. Take the plant material and convert it 1:1 into energy.
        """
        target_tile = self.get_current_tile()

        if target_tile.plant_material <= self.feed_amount:
            amt = target_tile.plant_material
        else:
            amt = self.feed_amount
            
        self.change_energy(amt)
        target_tile.change_plant_amount(-amt)
            