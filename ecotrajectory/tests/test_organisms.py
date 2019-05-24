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
def simple_creature_alt(simple_board):
    
    return org.Creature(location=(2,2), gameboard=simple_board, aggression=0.75,
                        speed=3, attack_power=20)

@pytest.fixture()
def simple_creature_alt2(simple_board):
    
    return org.Creature(location=(2,2), gameboard=simple_board, aggression=0.75,
                        speed=3, attack_power=25)

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

def test_Creature_overexertion_kills_self(simple_creature):

    simple_creature.change_energy(-55) # energy starts at 50
    assert simple_creature.is_alive == False

def test_Creature_die(simple_creature):

    simple_creature.die()
    assert simple_creature.is_alive == False

def test_Herbivore_eating_raises_energy(simple_herbivore):

    simple_herbivore.eat()
    assert np.isclose(simple_herbivore.energy, 55)
    # started at 50, should be 55 (5 plant available on tile, can get up to 10 at a time)

def test_Herbivore_eating_depletes_plant_matter(simple_herbivore):

    simple_herbivore.eat()
    plant = simple_herbivore.get_current_tile().plant_material
    assert plant == 0

def test_Creature_attack_hurts_target(simple_board):
    # creature attack power - 10
    # creature defense - 0.5
    # damage should be 10*0.5 == 5
    # creature inital vitality is 100
    creat1 = org.Creature(location=(2,2), gameboard=simple_board)
    creat2 = org.Creature(location=(2,2), gameboard=simple_board)
    creat1.attack(creat2)

    assert np.isclose(creat2.vitality, 95)

def test_Creature_attack_drains_own_energy(simple_board):
    # creature initial energy is 50
    # creature efficiency is 1, attack costs 5 energy
    creat1 = org.Creature(location=(2,2), gameboard=simple_board)
    creat2 = org.Creature(location=(2,2), gameboard=simple_board)
    creat1.attack(creat2)

    assert np.isclose(creat1.energy, 45)

def test_Creature_deathblow_kills_target(simple_board):
    # creature initial energy is vitality is 100
    # two attacks of power 100, with target defense 0.5 (50% damage reduction)
    # should kill
    creat1 = org.Creature(location=(2,2), gameboard=simple_board)
    creat2 = org.Creature(location=(2,2), gameboard=simple_board)
    creat1.attack_power = 100
    creat1.attack(creat2)
    assert creat2.is_alive == True
    creat1.attack(creat2)
    assert creat2.is_alive == False

def test_Creature_get_vals():

    creat = org.Creature(location=None, gameboard=None)
    expected = [100, 100, 10, 0.5, 0, 1, 0.8]

    assert creat.get_vals(creat.power_stats()) == expected

def test_Creature_power_score():

    creat = org.Creature(location=None, gameboard=None)
    expected = (3.458333333333334, 0.4940476190476191)

    assert np.allclose(creat.power_score(), expected)

def test_Creature_direction_to_location_straight_up(simple_creature):

    assert np.isclose(simple_creature.direction_to_location((2,3)), np.pi/2)

def test_Creature_direction_to_location_right(simple_creature):

    assert np.isclose(simple_creature.direction_to_location((3,2)), 0)

def test_Creature_direction_to_location_right_and_up(simple_creature):

    assert np.isclose(simple_creature.direction_to_location((3,3)), np.pi/4)

def test_Creature_direction_to_location_left_and_down(simple_creature):

    assert np.isclose(simple_creature.direction_to_location((1,1)), -(3/4)*np.pi)

def test_angle_between_points():

    ptA = (2,2)

    assert np.isclose(org.angle_between_points(ptA,(2,3)), np.pi/2)
    assert np.isclose(org.angle_between_points(ptA,(3,2)), 0)
    assert np.isclose(org.angle_between_points(ptA,(3,3)), np.pi/4)
    assert np.isclose(org.angle_between_points(ptA,(1,1)), -(3/4)*np.pi)

def test_angle_diff():

    assert np.isclose(org.angle_diff(np.pi/4,0), np.pi/4)
    assert np.isclose(org.angle_diff(np.pi,0), np.pi)
    assert np.isclose(org.angle_diff(-1,np.pi-1), np.pi)
    assert np.isclose(org.angle_diff(3*np.pi/4,np.pi/4), np.pi/2)
    assert np.isclose(org.angle_diff(3*np.pi/4,-3*np.pi/4), np.pi/2)

def test_get_closest_direction(simple_creature):
    # is on 2,2

    assert simple_creature.get_closest_direction((2,3)) == (0,1)
    assert simple_creature.get_closest_direction((3,2)) == (1,0)
    assert simple_creature.get_closest_direction((3,3)) == (1,1)
    assert simple_creature.get_closest_direction((4,4)) == (1,1)
    assert simple_creature.get_closest_direction((5,6)) == (1,1)
    assert simple_creature.get_closest_direction((1,1)) == (-1,-1)


def test_Creature_move_toward(simple_creature):
    # starts on 2,2
    simple_creature.move_toward((5,1))
    assert simple_creature.location == (3,2)

    simple_creature.move_toward((4,1))
    assert simple_creature.location == (4,1)

    simple_creature.move_toward((4,3))
    assert simple_creature.location == (4,2)

    simple_creature.move_toward((1,3))
    assert simple_creature.location == (3,2)
    
def test_Creature_move_randomly_raises_exception_when_no_valid_moves(simple_creature):
    
    simple_creature.location = (20,20) # out of bounds: any movement will throw error
    with pytest.raises(IndexError) as e_info:
        e = simple_creature.move_randomly()
    
def test_Creature_move_randomly_finds_path(simple_creature):
    for i in range(20):
        # test this 20 times to make sure it *probably* won't throw an error
        # this is a terrible testing pattern
        simple_creature.location = (0,0)
        simple_creature.move_randomly()
        
def test_Creature_combine_vals(simple_creature, simple_creature_alt):
    
    expected = {'maxenergy': 100,
                'maxvitality': 100,
                'attack_power': 15,
                'defense': 0.5,
                'efficiency': 0,
                'speed': 2,
                'fertility': 0.8,
                'aggression': 0.5}
    
    assert simple_creature.combine_vals(simple_creature_alt) == expected
    
def test_Creature_bring_stats_in_range():
    
    creat = org.Creature(location=None, gameboard=None,
                         maxenergy=5,
                         maxvitality=-5,
                         attack_power=300,
                         defense=1.5,
                         efficiency=0.5,
                         speed=1,
                         fertility=1,
                         aggression=3)
    
    expected = [5,0,300,0.8,0.5,1,1,1]
    creat.bring_stats_in_range()
    
    assert creat.get_vals(creat.mating_stats()) == expected
    
def test_Creature_normalize_power_stats():
    
    creat = org.Creature(None, None, maxenergy=200, maxvitality=100, attack_power=50,
                     defense=0.8, efficiency=0.8, speed=3, fertility=1)
    creat.normalize_power_stats()
    assert np.isclose(creat.power_score()[1], 1)
    
    expected = {'maxenergy': 100,
                'maxvitality': 100,
                'attack_power': 15,
                'defense': 0.5,
                'efficiency': 0,
                'speed': 2,
                'fertility': 0.8
               }
    expected = {key:val/(8/7) for key,val in expected.items()}
    assert creat.get_val_dict(creat.power_stats())
    
def test_Creature_mutate_attribute(simple_creature):
    
    simple_creature.mutate_attribute('maxvitality')
    simple_creature.mutate_attribute('aggression')
    with pytest.raises(KeyError) as e_info:
        e = simple_creature.mutate_attribute('location')
        
def test_Creature_reproduce(simple_creature, simple_creature_alt):
    
    a = simple_creature.reproduce(simple_creature_alt)
    
def test_Creature_mate(simple_creature, simple_creature_alt):
    
    simple_creature.fertility = 1
    simple_creature_alt.fertility = 1
    a = simple_creature.mate(simple_creature_alt)
    assert a is not None
    
    simple_creature.fertility = 1
    simple_creature_alt.fertility = 0
    a = simple_creature.mate(simple_creature_alt)
    assert a is None
    
def test_Creature_decay_removes_self_from_board(simple_creature):
    
    simple_creature.is_alive = False
    simple_creature.energy = 5
    simple_creature.decay()
    
    assert simple_creature not in simple_creature.gameboard.creatures
    
def test_remove_from_board(simple_board):
    
    a = org.Creature(location=(2,2), gameboard=simple_board)
    a.remove_from_board()
    
    assert simple_board.creatures == []
    
def test_Creature_same_species_at_loc(simple_board):
    
    a = org.Creature(location=(2,2), gameboard=simple_board)
    b = org.Creature(location=(2,2), gameboard=simple_board)
    c = org.Creature(location=(2,2), gameboard=simple_board)
    
    friends = a.same_species_at_loc(loc=(2,2))
    
    assert b in friends
    assert c in friends
    assert a not in friends

def test_Creature_try_to_mate_should_work(simple_board):
    
    a = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=200, efficiency=0, idTag='a')
    b = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=80, efficiency=0, idTag='b') # mating would kill
    c = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=60, efficiency=0.5, idTag='c') # mating would not kill
    
    did_mate = a.try_to_mate()
    assert did_mate == True
    
def test_Creature_try_to_mate_should_fail(simple_board):
    
    a = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=200, efficiency=0, idTag='a')
    b = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=80, efficiency=0, idTag='b') # mating would kill
    c = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=10, efficiency=0.5, idTag='c') # mating would not kill
    
    did_mate = a.try_to_mate()
    assert did_mate == False

def test_Creature_potential_mates(simple_board):
    
    a = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=200, efficiency=0, idTag='a')
    b = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=80, efficiency=0, idTag='b') # mating would kill
    c = org.Creature(location=(2,2), gameboard=simple_board, maxenergy=60, efficiency=0.5, idTag='c') # mating would not kill
    d = org.Creature(location=(2,3), gameboard=simple_board, maxenergy=200, efficiency=0, idTag='d') # wrong tile

    potential_mates = a.potential_mates()
    
    assert a not in potential_mates
    assert b not in potential_mates
    assert c in potential_mates
    assert d not in potential_mates
    
    b.efficiency = 0.7 # efficient enough to mate with current energy
    c.energy = 25 # right at the threshold - this mating will now kill it
    d.location = (2,2) # onto the right indices

    potential_mates = a.potential_mates()
    
    assert b in potential_mates
    assert c not in potential_mates
    assert d in potential_mates
    