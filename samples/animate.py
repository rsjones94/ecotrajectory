"""
A sample ecosystem
"""

import sys
sys.path.append('..')

from celluloid import Camera as cam

import matplotlib.pyplot as plt

fig = plt.figure()
camera = cam(fig)
plt.xlabel('Turn')
plt.ylabel('Creatures Alive')

for i in range(1,len(turns),10):
    plt.plot(turns[0:i], game.statdict['herbivore']['alive'][0:i],color='red')
    plt.plot(turns[0:i], game.statdict['predator']['alive'][0:i],color='blue')
    camera.snap()
    
animation = camera.animate()
animation.save(r'C:\Users\rsjon_000\Documents\ecotrajectory\samples\tester.gif',)