"""
Various kinds of organisms for use in the simulation.
"""

MOVEMENT_COST = 10
ATTACK_COST = 5
MATING_COST = 25

class Creature():
    
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
            self.energy -= MOVEMENT_COST*self.efficiency
        else:
            raise IndexError(f'Creature cannot move to {new_pos}')
            
    def die(self):
        
        self.is_alive = False
        
    def get_current_tile(self):
        
        return self.gameboard.landscape[self.location[0],
                                        self.location[1]]

        

class Herbivore(Creature):
    
    feed_amount = 10
    
    """
    They just like eatin' plants.
    
    Attributes:
        feed_amount(float): the amount of energy that can be converted in a
            single feeding
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
        if target_tile.plant_material <= 0:
            pass
        elif target_tile.plant_material <= self.feed_amount:
            self.energy += target_tile.plant_material
            target_tile.plant_material = 0
        else:
            self.energy += self.feed_amount
            target_tile.plant_material -= self.feed_amount
            