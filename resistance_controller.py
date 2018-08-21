"""
Use the semiprober to take resistance measurements of a dye of nanowires at 300K
"""

import Semiprobe as sp
import Keithley2400 as k2
import csv, datetime

name = 'CHIP NAME'
now = datetime.datetime.now().isoformat()[:16]
port = '/dev/prologix0'
l = k24.dev(1, port)
with open('nanowire_res_%s_%s.csv' %(name, now), 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    LED_locations = [] #tuples [x,y] either by hand or from phidl
    zero_loc = LED_location[0] #set 0 coordinate. start the autoprober here
    for loc in LED_locations:
        sp.separation() #move the probs away
        sp.moveAbs(loc[0]-zero_loc[0],loc[1]-zero_loc[1]) #move to next location
        sp.contact() #contact pads
        data = l.get_R() #take resitance measurment
        
        writer.writerow([loc]) #write location and data to file
        writer.writerow(data)