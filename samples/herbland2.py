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
logging.basicConfig(filename=r'C:\Users\rsjon_000\Desktop\herbland12.log',level=logging.INFO)



game = ply.Player(n_herbivores=25, n_predators=6, tile=env.Forest(), boardsize=(8,8),
                  turns=500, record_every=10)

game.execute()



turns = game.statdict['turn']

for key in game.statdict['herbivore']:
    plt.figure()
    plt.plot(turns,game.statdict['herbivore'][key])
    try:
        plt.plot(turns,game.statdict['predator'][key])
    except KeyError:
        pass
    plt.title(key)
    plt.legend()