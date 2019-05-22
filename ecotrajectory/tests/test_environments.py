"""
Tests for environments.py using pytest
"""

import pytest

from .. import environments as env


def test_Gameboard_create_landscape():
    
    board = env.Gameboard(boardsize=(4,6), tile=env.Prarie)
    assert board.create_landscape().shape == (4,6)
    
def test_Tile_plant_grow():
    
    tile = env.Tile(max_plant_material=10, plant_material=7,
                    plant_growth_rate=2, organisms=[])
    tile.plant_grow()
    
    assert tile.plant_material == 9
    
def test_Tile_plant_grow_no_overflow():
    
    tile = env.Tile(max_plant_material=10, plant_material=9,
                    plant_growth_rate=2, organisms=[])
    tile.plant_grow()
    
    assert tile.plant_material == 10