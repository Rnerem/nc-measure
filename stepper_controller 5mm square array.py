"""
Master code to automatically take iv curves of many LEDs using the auto prober
"""

import Semiprobe #Semiprobe commands module
sp = Semiprobe.prober() #sp is instance of prober object
import z_iv
import csv, datetime, numpy

# x,y coords of contact pads RELATIVE to PREVIOUS position
# set probe to first device before running
LEDlocRel = [[0,0],[900,0],[900,0],[900,0],[900,0],[0,350],[-900,0],[-900,0],[-900,0],[-900,0],[0,450],[900,0],[900,0],[900,0],[900,0],[0,550],[-900,0],[-900,0],[-900,0],[-900,0],[0,650],[900,0],[900,0],[900,0],[900,0]] #top 5 rows
numDevs = len(LEDlocRel)

startPt = sp.getPos() #returns x,y position as [x,y]

name = 'AsP339_IV_bksdAnn2'
now = datetime.datetime.now().isoformat()[:13]
vStart = -1
vStop = 3
vStep = 0.01
numDataPts = int((vStop - vStart)/vStep)
dataMat = numpy.zeros((numDataPts,numDevs*2))
           
for ii in range(numDevs):
    sp.seperation() # moves Z position of stage to separation height
    loc = LEDlocRel[ii]
    sp.moveRel(loc[0],loc[1],20) # moves x,y position relative to current position, i.e. moveRel(100,100,20) moves +100 in x and y at speed 20
    sp.contact() # moves Z position of stage to contact height
    data = z_iv.measure_V(vStart,vStop,vStep)
    
    dataMat[:,ii*2] = data[0]
    dataMat[:,ii*2+1] = data[1]
    
    print('{a}%'.format(a=ii/numDevs))
       
sp.seperation()
sp.moveAbs(startPt[0],startPt[1]) # Returns to starting position in absolute [x,y] coords
z_iv.l.beep()

with open('_%s_%s.csv' %(name,now), 'w') as csvfile:
    writer = csv.writer(csvfile,delimiter = ',',quoting = csv.QUOTE_MINIMAL)
    for ii in range(int(numDataPts)):
        writer.writerow(dataMat[ii,:])
        