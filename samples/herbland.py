"""
A sample ecosystem
"""

import sys
sys.path.append('..')
import random
import logging

import numpy as np
import matplotlib.pyplot as plt

import ecotrajectory.organisms as org
import ecotrajectory.environments as env

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=r'C:\Users\rsjon_000\Desktop\herbland.log',level=logging.WARNING)


board = env.Gameboard(boardsize=(10,10), tile=env.Prarie())

for i in range(2):
    a = org.Herbivore(location=(random.randint(0,2),random.randint(0,2)),
                      gameboard=board,
                      idTag=i
                     )
    
alive = []
dead = []
avgEnergy = []
avgSpeed = []
avgEfficiency = []
avgFertility = []    
    
for i in range(10000):
    logging.info(f'\n--- turn {i} ---\n')
    board.play()
    
    alive.append(len(board.creatures))
    dead.append(len(board.removed_creatures))
    avgEnergy.append(np.mean([c.maxenergy for c in board.creatures]))
    avgSpeed.append(np.mean([c.speed for c in board.creatures]))
    avgEfficiency.append(np.mean([c.efficiency for c in board.creatures]))
    avgFertility.append(np.mean([c.fertility for c in board.creatures]))
    
plt.figure()
plt.plot(alive)
plt.title('alive')

plt.figure()
plt.plot(dead)
plt.title('dead')

plt.figure()
plt.plot(avgEnergy)
plt.title('avgEnergy')

plt.figure()
plt.plot(avgEfficiency)
plt.title('avgEfficiency')

plt.figure()
plt.plot(avgFertility)
plt.title('avgFertility')
