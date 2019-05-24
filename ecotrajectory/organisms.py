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
    #'maxenergy', 'maxvitality', 'attack_power', 'defense', 'efficiency', 'speed'
    #'fertility'
    PERFECT_STATS = [200, 100, 50, .8, .8, 3, 1]
    #'maxenergy', 'maxvitality', 'attack_power', 'defense', 'efficiency', 'speed'
    #'fertility', 'aggression'
    STAT_RANGES = {'maxenergy':(0,float('inf')),
                   'maxvitality':(0,float('inf')),
                   'attack_power':(0,float('inf')), 
                   'defense':(0,0.8),
                   'efficiency':(0,0.8),
                   'speed':(0,float('inf')),
                   'fertility':(0,1),
                   'aggression':(0,1)
                  }
    MUTATION_CHANCE = 0.01
    
    """
    An animal-esque creature to be placed on a Gameboard.
    
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
        STAT_RANGES(dict of tuples of float): min and max possible values
            for mating attributes
        MUTATION_CHANCE(float): the probability a mutation will occur for an attribute
            during reproduction
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
        self.movements_left = speed
        
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
    
    def get_val_dict(self, atts):
        
        return {key:val for key,val in zip(atts,self.get_vals(atts))}
        
    def power_score(self):
        """
        Generate a score that assesses the overall power of a creature.
        Normalizes Creature attributes against "perfect attributes" and then
        sums the scores.
        
        Returns:
            A tuple of two numbers. The first is the absolute power score.
            The second is the relative power score (ratio of absolute score to
            a perfect score). A 1 is a "perfect" score but not the max. Scores over
            one are normalized for offspring produced by mating.
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
    
    def combine_vals(self, target):
        """
        Create a dictionary that averages mating values between self and a
        target Creature
        """
        
        own_vals = self.get_vals(self.mating_stats())
        target_vals = target.get_vals(target.mating_stats())
        offspring_vals = [(o+t)/2 for o,t in zip(own_vals,target_vals)]

        val_dict = {stat:val for stat,val in zip(self.mating_stats(),offspring_vals)}
        return val_dict
    
    def bring_stats_in_range(self):
        """
        Takes all mating attributes and makes them fit into the possible ranges
        """
        
        current_vals = self.get_val_dict(self.mating_stats())
        for key in self.STAT_RANGES:
            if current_vals[key] < self.STAT_RANGES[key][0]:
                setattr(self, key, self.STAT_RANGES[key][0])
            if current_vals[key] > self.STAT_RANGES[key][1]:
                setattr(self, key, self.STAT_RANGES[key][1])
                
    def normalize_power_stats(self):
        """
        Scales the power attributes so that the normalized power_score is 1
        """
        
        norm_score = self.power_score()[1]
        if norm_score> 1:
            for key,val in self.get_val_dict(self.power_stats()).items():
                setattr(self, key, val/norm_score)
                
    def mutate_attribute(self,attr):
        """
        Takes an attriute and adds or takes away a random amount (scaled to
        the possible ranges the attribute can have)
        """
        
        stat_range = self.STAT_RANGES[attr]
        if stat_range[1] == float('inf'):
            factor = 100
        else:
            factor = stat_range[1] - stat_range[0]
            
        mutation_amount = factor*random.uniform(-1,1)
        setattr(self, attr, getattr(self, attr)+mutation_amount)
        
    def reproduce(self, target):
        """
        Produce an offspring with another Creature
        """
        
        offspring_stats = self.combine_vals(target)
        offspring = type(self)(location=self.location,
                               gameboard=self.gameboard,
                               maxenergy=offspring_stats['maxenergy'],
                               speed=offspring_stats['speed'],
                               efficiency=offspring_stats['efficiency'],
                               maxvitality=offspring_stats['maxvitality'],
                               attack_power=offspring_stats['attack_power'],
                               defense=offspring_stats['defense'],
                               fertility=offspring_stats['fertility'],
                               aggression=offspring_stats['aggression'])
        
        for key in offspring.mating_stats(): # randomly mutate attributes
            mut_num = random.uniform(0,1)
            if mut_num >= self.MUTATION_CHANCE:
                offspring.mutate_attribute(key)
                
        offspring.normalize_power_stats() # keep offspring from getting too powerful
        
        return offspring
    
    def mate(self, target):
        
        if random.uniform(0,1) > (1-self.fertility) and random.uniform(0,1) > (1-target.fertility):
            return self.reproduce(target)
    
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
            