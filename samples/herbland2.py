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
logging.basicConfig(filename=r'C:\Users\rsjon_000\Desktop\herbland30.log',level=logging.INFO)



game = ply.Player(n_herbivores=100, n_predators=15, tile=env.Prarie(), boardsize=(30,30),
                  turns=10000, record_every=1)

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