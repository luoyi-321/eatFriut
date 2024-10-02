import os
import random

class Object:
    
    def __init__(self):
        self.posx         = random.randint(10,540)
        self.posy         = 0
        self.isEatable    = False
        self.eated        = False
        self.objDIR       = Object.loadDir()
        
    
    def loadDir(self):
        if random.randint(0,1) == 0:
            DIR = "eatFruitGame\object\eatable" 
        else :
            DIR = "eatFruitGame\object\\noneatable"
        return DIR
    def objMove(self):
        pass
    def objectReset(self):
        pass
