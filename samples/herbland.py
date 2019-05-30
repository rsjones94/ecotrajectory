"""
A sample ecosystem
"""

import sys
sys.path.append('..')
import random
import logging
import time

import numpy as np
import matplotlib.pyplot as plt

import ecotrajectory.organisms as org
import ecotrajectory.environments as env

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=r'C:\Users\rsjon_000\Desktop\herbland.log',level=logging.WARNING)

the_size = (4,4)
loc = (the_size[0]-1, the_size[1]-1)

tracker = 100
sim_length = 15000

n_creatures = 3



board = env.Gameboard(boardsize=the_size, tile=env.Prarie())

for i in range(n_creatures):
    a = org.Herbivore(location=(random.randint(loc[0],loc[1]),random.randint(loc[0],loc[1])),
                      gameboard=board)

