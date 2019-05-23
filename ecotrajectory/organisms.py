"""
Various kinds of organisms for use in the simulation.
"""

import math

class Creature():
    
    MOVEMENT_COST = -10
    ATTACK_COST = -5
    MATING_COST = -25
    
    """
    An animal-esque creater to be placed on a Gameboard.
    
    Attributes:
        energy(float): the energy the creature has for tasks
        speed(int): the number of movements a creature gets per turn
        actions(int): the number of non-movement actions a creature gets per turn
        efficiency(float): the efficiency with which the creature performs tasks
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
    """
    
    def __init__(self, location, gameboard, maxenergy=100, speed=1, efficiency=1,
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
            self.energy += self.MOVEMENT_COST*self.efficiency
        else:
            raise IndexError(f'Creature cannot move to {new_pos}')
            
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
        
        self.energy += amount
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
        
        self.change_vitality(-amount*self.defense)
        
    def power_stats(self):
        """
        Returns a list of attributes relevant to calculating power scores
        """
        
        return ['maxenergy', 'maxvitality', 'attack_power', 'defense',
                'efficiency', 'speed', 'fertility']
        
    def power_vals(self):
        """
        Returns a list of values corresponding to the attributes returned by
        power_stats
        """
        
        return [getattr(self,l) for l in self.power_stats()]
        
    def perfect_stats(self):
        """
        Returns a list of ideal scores for the attributes returned by
        power_stats
        """
        
        # we take the inverse of defense and efficiency as lower scores are better
        return [200, 100, 50, 1/0.2, 1/0.2, 3, 1]
        
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
                  zip(self.power_vals(),self.perfect_stats())]
        
        power_score = sum(scores)
            
        return power_score, power_score/len(scores)
    
    def angle_to_location(self, loc):
        """
        Get the angle in radians between the x-axis and the vector connecting
        the current location to another location, loc (x,y)
        
        Vectors in quadrants 1 and 2 have positive angles
        Vectors in quadrants 3 and 4 have negative angles
        """
        
        delta_x = loc[0] - self.location[0]
        delta_y = loc[1] - self.location[1]
        return math.atan2(delta_y, delta_x)

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
                                        efficiency=1,
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
            