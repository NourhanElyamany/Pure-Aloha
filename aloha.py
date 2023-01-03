import numpy
import math
import random

class node:
    def __init__(self, status =  'inactive', packets = 1):
        self.status = status
        self.packets = packets

    
    
def effiency(nodes):
    
    return nodes * math.exp(-2 * nodes)

def state():
    if random.choice(['active', 'inactive']) == 'active':
        return True
    return False
    
    
    
#def poisson_distribution():
  