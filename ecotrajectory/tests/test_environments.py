"""
Tests for environments.py using pytest
"""

import pytest

from .. import environments as env

@pytest.fixture()
def simple_board():
    
    return env.Gameboard(boardsize=(10,5), tile=env.Prarie)

### end fixtures ###

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