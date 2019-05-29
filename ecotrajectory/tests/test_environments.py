"""
Tests for environments.py using pytest
"""

import pytest

from .. import environments as env
from .. import organisms as org

@pytest.fixture()
def simple_board():
    
    return env.Gameboard(boardsize=(10,5), tile=env.Prarie)

@pytest.fixture()
def simple_creature(simple_board):

    return org.Creature(location=(2,2), gameboard=simple_board)

@pytest.fixture()
def simple_creature_alt(simple_board):
    
    return org.Creature(location=(2,2), gameboard=simple_board, aggression=0.75,
                        speed=3, attack_power=20)

### end fixtures ###

def test_Gameboard_add_to_board(simple_board):
    
    a = 'test'
    simple_board.add_to_board(a)
    assert a in simple_board.creatures
    
def test_Gameboard_remove_from_board(simple_board):
    
    a = 'test'
    
    simple_board.add_to_board(a)
    simple_board.remove_from_board(a)
    
    assert a not in simple_board.creatures
    assert a in simple_board.removed_creatures

def test_Gameboard_create_landscape():
    
    board = env.Gameboard(boardsize=(4,6), tile=env.Prarie)
    assert board.create_landscape().shape == (4,6)
    
def test_Tile_plant_grow():
    
    tile = env.Tile(max_plant_material=10, plant_material=7,
                    plant_growth_rate=2)
    tile.plant_grow()
    
    assert tile.plant_material == 9
    
def test_Tile_plant_grow_no_overflow():
    
    tile = env.Tile(max_plant_material=10, plant_material=9,
                    plant_growth_rate=2)
    tile.plant_grow()
    
    assert tile.plant_material == 10
    
def test_Gameboard_pos_is_valid(simple_board):
    
    assert simple_board.pos_is_valid((0, 0)) == True
    assert simple_board.pos_is_valid((-1, 0)) == False
    assert simple_board.pos_is_valid((2, 3)) == True
    assert simple_board.pos_is_valid((4, 4)) == True
    assert simple_board.pos_is_valid((5, 4)) == True
    assert simple_board.pos_is_valid((4, 5)) == False

def test_Gameboard_creatures_at_index(simple_board,
                                      simple_creature,
                                      simple_creature_alt):
    
    assert len(simple_board.creatures_at_index(index=(2,2))) == 2