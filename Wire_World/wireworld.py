from wwlib import *
from boards import *
from time import sleep
import os

WW=wireworld(0, 0, Circle)

"""
C.setPos(10,10,1)
C.setPos(9,10,1)
C.setPos(12,10,1)
C.setPos(10,9,1)
C.setPos(11,9,1)
C.setPos(10,11,1)
C.setPos(11,11,1)

C.setPos(10,20,1)
C.setPos(11,21,1)
C.setPos(12,19,1)
C.setPos(12,20,1)
C.setPos(12,21,1)
"""

n = 0
while True:
   os.system('clear')
   WW.Display()
   print "STEP:",n
   sleep(0.5)
   WW.evolve(rule)
   n = n+1
