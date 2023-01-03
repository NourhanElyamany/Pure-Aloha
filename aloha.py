import numpy
import math

class node:
    def __init__(self, status =  'inactive', packets = 1):
        self.status = status
        self.packets = packets

    
    
def effiency(nodes):
    
    return nodes * math.exp(-2 * nodes)
    
def poisson_distribution():
  