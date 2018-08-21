# -*- coding: utf-8 -*-
"""
Semiprobe prober control software
Started 2-8-2017
MLS
"""


import pyvisa

from MeasureUtils import fullSleep
#from pyvisa.compat.struct import unpack, unpack_from
import numpy as np

port='GPIB0::5'


class prober(): 
    def __init__(self):
        self.port = port
        rm = pyvisa.ResourceManager()
        self.inst = rm.open_resource(self.port, read_termination = '\n', write_termination='\n', timeout=30000, query_delay=0.1)

        print('Prober Name Test ',self.inst.query('*IDN?'))    
        fullSleep(1)
     

    
    def cls(self):
        self.inst.write('*CLS')
        #self.inst.write('1')
        fullSleep(1)
        print('cls')
        #self.inst.write('*CLS')
        #fullSleep(1)

    def idn(self):
        print('idn')
        print(self.inst.write('*IDN?'))
        fullSleep(1)
        print(self.inst.read())
        fullSleep(1)
        print('idn done')
        
    
    ### semiprobe prober commands ####        
    def moveAbs(self, x=0,y=0,speed=50):
        mov = self.inst.query('PIMoveXYAbsolute {} {} {}'.format(x,y,speed))
        fullSleep(2)
        print(mov)
        
    def moveRel(self,x=0,y=0,speed=50):
        currPos = self.getPos()
        mov = self.inst.query('PIMoveXYAbsolute {} {} {}'.format(currPos[0]+x,currPos[1]+y,speed))
        print(mov)
        

    def getPos(self):
        pos = self.inst.query('PIGetXYPosition')[27:]
        xCurr = float(pos[3:(pos.find('Y'))])
        yCurr = float(pos[(pos.find('Y')+3):(pos.find('\\'))])
        
        return [xCurr,yCurr]

    def contact(self):
        con = self.inst.query('PIMoveZContact')
        fullSleep(0.3)
        print(con)
        
    def seperation(self):
        sep = self.inst.query('PIMoveZSeparation')
        fullSleep(0.3)
        print(sep)
        return sep