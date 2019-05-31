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



game = ply.Player(n_herbivores=10, n_predators=0, tile=env.Forest(), boardsize=(5,5),
                  turns=10000, record_every=100)

game.execute()



turns = game.statdict['turn']

for key,val in game.statdict['herbivore'].items():
    plt.figure()
    plt.plot(turns,val)
    plt.title(key)
