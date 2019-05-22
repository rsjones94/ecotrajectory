"""
Classes to make the "gameboard" that the simulation will run on.
"""

import numpy as np


class GameBoard():

    """
    A raster-like board composed of environmental Tiles.

    Attributes:
        size(tuple): a len 2 tuple specify the x-y dimensions of the gameboard
        tile(Environment): an Environment tile that the board will be composed of
        """

    def __init__(self, size, tile):
        
        self.size = size
        self.tile = tile
    
    def create_landscape(self):
        
        row = [self.tile for l in range(self.size[0])]
        landscape = [row for l in range(self.size[1])] 
        self.landscape = np.matrix(landscape)
        

class Tile():
    
    """
    A tile that represents a type of environment.
    
    Attributes:
        max_plant_material(float): the max amount of plant growth on a tile
        plant_material(float): the amount of plant material on the tile
        plant_growth_rate(float): the rate at which plant matter grows on the tile per cycle
        organisms(:obj:'list' of :obj:'Organism'): organisms present on the tile
    """

    def __init__(self, max_plant_material, plant_material, plant_growth_rate, organisms=[]):
        
        self.max_plant_material = max_plant_material
        self.plant_material = plant_material
        self.plant_growth_rate = plant_growth_rate
        self.organisms = organisms
        
    def plant_grow(self):
        """
        Grows the plants on the tile.
        """
        
        self.plant_material += self.plant_growth_rate
        if self.plant_material > self.max_plant_material:
            self.plant_material = self.max_plant_material
        

class Prarie(Tile):
    
    """
    A prarie Title.
    """
    
    def __init__(self):
        super(Prarie, self).__init__(max_plant_material=10, plant_material=5,
                                     plant_growth_rate=1, organisms=[])