from conwaylib import *
from random import randint
from time import sleep
import os

r=40
c=30
C=conway(r,c,False)

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

n = 0
while True:
   C.evolve(rule)
   os.system('clear')
   C.Display()
   print "STEP:",n
   sleep(0.05)
   n += 1
