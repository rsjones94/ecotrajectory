import os
import random

selfloc = os.path.dirname(os.path.realpath(__file__))
name = r'words.txt'
file = os.path.join(selfloc,name)

with open(file) as words:
    word_list = words.read().split('\n')

def generate_name(n=3):
    global word_list
    words = random.choices(word_list, k=n)
    words = [w.capitalize() for w in words]
    return ''.join(words)
    
