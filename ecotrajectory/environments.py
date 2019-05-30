"""
Classes to make the "gameboard" that the simulation will run on.
"""

from copy import deepcopy

import numpy as np


class Gameboard():

    """
    A raster-like board composed of environmental Tiles.

    Attributes:
        boardsize(tuple): a len 2 tuple (x,y) specify the number of rows y and columns x
        tile(Environment): an Environment tile that the board will be composed of
        landscape(numpy array of tile): a landscape of tiles covering the gameboard
        creatures(list of Creatures): a list of Creature objects on the board
        removed_creatures(list of Creatures): a list of Creature objects that have been
            removed from the board
        """

    def __init__(self, boardsize, tile):
        
        self.boardsize = boardsize
        self.tile = tile
        self.landscape = self.create_landscape()
        self.creatures = []
        self.removed_creatures = []
        
    def play(self):
        """
        Let everyone take a turn.
        """
        for creature in self.creatures.copy():
            assert all(c.is_alive for c in self.creatures)
            creature.take_turn()
        for row in self.landscape:
            for tile in row:
                tile.plant_grow()
        
    def create_landscape(self):
        
        row = [deepcopy(self.tile) for l in range(self.boardsize[1])]
        landscape = [deepcopy(row) for l in range(self.boardsize[0])] 
        return np.array(landscape)
    
    def pos_is_valid(self, pos):
        """
        Returns if a position (x,y) is valid on the board.
        """
        xMax = self.landscape.shape[0]-1
        yMax = self.landscape.shape[1]-1
        if not(pos[0] >= 0 and pos[0] <= xMax):
            return False
        if not(pos[1] >= 0 and pos[1] <= yMax):
            return False
        
        return True
    
    def add_to_board(self, target):
        """
        Add a creature to the board
        """
        self.creatures.append(target)
        
    def remove_from_board(self, target):
        """
        Add a creature to the board
        """
        self.creatures.remove(target)
        self.removed_creatures.append(target)
        
    def creatures_at_index(self, index):
        """
        Returns all creatures currently at an index
        """
        return [creature for creature in self.creatures
                if creature.location == index]
        

class Tile():
    
    """
    A tile that represents a type of environment.
    
    Attributes:
        max_plant_material(float): the max amount of plant growth on a tile
        plant_material(float): the amount of plant material on the tile
        plant_growth_rate(float): the rate at which plant matter grows on the tile per cycle
        """

    def __init__(self, max_plant_material, plant_material, plant_growth_rate):
        
        self.max_plant_material = max_plant_material
        self.plant_material = plant_material
        self.plant_growth_rate = plant_growth_rate
        
    def plant_grow(self):
        """
        Grows the plants on the tile.
        """
        self.change_plant_amount(self.plant_growth_rate)
            
    def change_plant_amount(self, amount):
        """
        Alter the plant matter on the Tile
        """
        self.plant_material += amount
        
        if self.plant_material > self.max_plant_material:
            self.plant_material = self.max_plant_material
        elif self.plant_material < 0:
            self.plant_material = 0
        

class Prarie(Tile):
    
    """
    A prarie Title.
    """
    
    def __init__(self):
        super(Prarie, self).__init__(max_plant_material=25, plant_material=10,
                                     plant_growth_rate=5)
        
class Forest(Tile):
    
    """
    A forest Title.
    """
    
    def __init__(self):
        super(Forest, self).__init__(max_plant_material=50, plant_material=20,
                                     plant_growth_rate=8)
        
class Desert(Tile):
    
    """
    A desert Title.
    """
    
    def __init__(self):
        super(Desert, self).__init__(max_plant_material=10, plant_material=5,
                                     plant_growth_rate=2)
        
class Wasteland(Tile):
    
    """
    A wasteland Title.
    """
    
    def __init__(self):
        super(Wasteland, self).__init__(max_plant_material=0, plant_material=0,
                                     plant_growth_rate=0)