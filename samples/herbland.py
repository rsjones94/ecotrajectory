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

tracker = 500
sim_length = 100000

n_creatures = 3



sim_start = time.time()
board = env.Gameboard(boardsize=the_size, tile=env.Prarie())

for i in range(n_creatures):
    a = org.Herbivore(location=(random.randint(loc[0],loc[1]),random.randint(loc[0],loc[1])),
                      gameboard=board)
     
turn = []
alive = []
dead = []
avgEnergy = []
avgSpeed = []
avgEfficiency = []
avgFertility = []   

start = time.time()
for i in range(sim_length):
    logging.info(f'\n--- turn {i} ---\n')
    board.play()
    
    if i%tracker == 0:
        end = time.time()
        print(f'Turn {i}. Time between {tracker} turns: {round(end-start,2)}')
        start = time.time()
        
        aliveC = [c for c in board.creatures if c.is_alive]
        deadC = board.removed_creatures
        deadC.extend([c for c in board.creatures if not c.is_alive])
    
        turn.append(i)
        alive.append(len(aliveC))
        dead.append(len(deadC))
        avgEnergy.append(np.mean([c.maxenergy for c in aliveC]))
        avgSpeed.append(np.mean([c.speed for c in aliveC]))
        avgEfficiency.append(np.mean([c.efficiency for c in aliveC]))
        avgFertility.append(np.mean([c.fertility for c in aliveC]))
        
sim_end = time.time()

print(f'Simulation finished. Elapsed time: {round(end-start,2)}')
    
plt.figure()
plt.plot(turn,alive)
plt.title('alive')

plt.figure()
plt.plot(turn,dead)
plt.title('dead')

plt.figure()
plt.plot(turn,avgEnergy)
plt.title('avgEnergy')

plt.figure()
plt.plot(turn,avgEfficiency)
plt.title('avgEfficiency')

plt.figure()
plt.plot(turn,avgFertility)
plt.title('avgFertility')
