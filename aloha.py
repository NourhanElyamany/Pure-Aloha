import numpy
import math
import random


class node:
    def __init__(self, status =  'inactive', packets = 2):
        self.status = status
        self.packets = packets

    
    
def effiency(nodes):
    
    return nodes * math.exp(-2 * nodes)

def state():
    if random.choice(['active', 'inactive']) == 'active':
        return True
    return False

def transmission(nodes):
    actives = []
    for i in range(1,nodes):    #node creation  
        
        if state() == True:
            node().status = 'active'
            actives.append(node())
        
        
 
nodes = 3

print(transmission(nodes))
   
    
    
#def poisson_distribution():
  