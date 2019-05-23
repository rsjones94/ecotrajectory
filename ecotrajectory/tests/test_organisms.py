"""
Tests for environments.py using pytest
"""

import numpy as np
import pytest

from .. import organisms as org
from .. import environments as env


@pytest.fixture()
def simple_board():
    
    return env.Gameboard(boardsize=(10,5), tile=env.Prarie())

@pytest.fixture()
def simple_creature(simple_board):
    
    return org.Creature(location=(2,2), gameboard=simple_board)

@pytest.fixture()
def simple_herbivore(simple_board):
    
    return org.Herbivore(location=(2,2), gameboard=simple_board)

### end fixtures ###

def test_Creature_move(simple_creature):

    simple_creature.move(delX=1, delY=1) # new pos - 3,3
    simple_creature.move(delX=0, delY=1) # new pos - 3,4
    with pytest.raises(IndexError) as e_info:
        e = simple_creature.move(delX=0, delY=1) # new pos - 3,5 (out of bounds)
        
def test_Creature_move_costs_energy(simple_creature):
    
    simple_creature.move(delX=1, delY=1) # energy starts at 50, this should cost 10
    assert np.isclose(simple_creature.energy, 40)
    
def test_Creature_die(simple_creature):
    
    simple_creature.die()
    assert simple_creature.is_alive == False
    
def test_Creature_grazing_raises_energy(simple_herbivore):
    
    simple_herbivore.graze()
    assert np.isclose(simple_herbivore.energy, 55) 
    # started at 50, should be 55 (5 plant available on tile, can get up to 10 at a time)
    
def test_Creature_grazing_depletes_plant_matter(simple_herbivore):
    
    simple_herbivore.graze()
    plant = simple_herbivore.get_current_tile().plant_material
    assert plant == 0
