# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 12:24:01 2017
see similar iv.py

@author: zsteffen
"""

#import Keithley2400 as k24
import Keithley2400_pyvisa as k24
import numpy as np
import matplotlib.pyplot as pplt
import time,csv

l = k24.dev(2)



def measure_V(vstart,vstop,vstep,speed = 1,prot = 1e-6):
    # addr = 'dev1'
    # l = k24.dev(addr,1) #creates a Keithley2400 object
#    port = '/dev/prologix0'
#    l = k24.dev(1, port) #creates a Keithley2400 object
#    l = k24.dev(2)
    """
    vmax = vstop
    pausetime = 1
    v_setpnts_up = np.arange(vstart, vmax+vstep, vstep)
    v_setpnts_down = np.arange(vmax, vstart-vstep, vstep)
    
    l.output_on()
    l.set_V(vstart)
    time.sleep(1)
    data = []
    for v_set in v_setpnts_up:
        l.set_V(v_set)
        time.sleep(.1)
        vact = l.get_V()
        iact = l.get_I()
        d = [vact,iact]
        data.append(d)
    """
    data = l.sweep_V(vstart,vstop,vstep,speed) #sweeps the given range
    data = data.split(',')
    v = data[0::5] 
    c = data[1::5]
    data = [v,c]
    dtemp = []
    for row in data:
        #print(row)
        row = [float(s) for s in row]
        dtemp.append(row)
    data = dtemp
    #l.set_V()
    #l.meter.close()
#    l.beep()
    return data #returns voltage and current from the sweep    

def measure_I(istart,istop,istep,speed = 1):
    addr = 'dev1'
    l = k24.dev(addr,1)
    data = l.sweep_I(istart,istop,istep,speed)
    data = data.split(',')
    v = data[0::5] 
    c = data[1::5]
    l.set_V()
    l.meter.close()
    return [v, c]
    
def plot_V(vstart,vstop,vstep): 
    [v,c] = measure_V(vstart,vstop,vstep)
    #res = (v[5]-v[4])/(c[5]-c[4])
    pplt.figure(1)
    pplt.clf()
    pplt.plot(v,c,'ro')
    #pplt.axis([0,1,0,1e-4])
    pplt.xlabel('Volts')
    pplt.ylabel('Amps')
    pplt.title('I-V')
    #note = 'Resistence: %f' %res
    #pplt.text(-.5,5e-5,note)
    pplt.grid(True)
    pplt.ion()
    pplt.show()
    
def save_V(vstart,vstop,vstep,filename):
    data = measure_V(vstart,vstop,vstep)
    
    
    
    with open(filename+'.csv', 'w') as csvfile:
        writer = csv.writer(csvfile,delimiter = ',',quoting = csv.QUOTE_MINIMAL)
        for ii in range(len(data[0])):
            writer.writerow([data[0][ii],data[1][ii]])
            
    pplt.plot(data[0],data[1],'ro')
    pplt.show()