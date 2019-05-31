"""
A sample ecosystem
"""

import sys
sys.path.append('..')
import logging

import matplotlib.pyplot as plt

import ecotrajectory.environments as env
import ecotrajectory.player as ply

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=r'C:\Users\rsjon_000\Desktop\herbland3.log',level=logging.WARNING)



game = ply.Player(n_herbivores=10, n_predators=5, tile=env.Forest(), boardsize=(6,6),
                  turns=1000, record_every=1000)

game.execute()


"""
turns = game.statdict['turn']

for key,val in game.statdict['herbivore'].items():
    plt.figure()
    plt.plot(turns,val)
    plt.title(key+ ': herbivore')
    
for key,val in game.statdict['predator'].items():
    plt.figure()
    plt.plot(turns,val)
    plt.title(key+ ': predator')
"""

game.initialize_statistics_dictionary()
game.record_statistics(0)