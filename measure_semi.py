import ruamel.yaml
yaml = ruamel.yaml.YAML(typ='unsafe')
import numpy as np
import Keithley2400_pyvisa as k24
k = k24.dev(2)
import Semiprobe #Semiprobe commands module
sp = Semiprobe.prober() #sp is instance of prober object

stream = open('/home/linaro/nc-phidl/die/WB_info.yaml','r')
info = yaml.load(stream)

dev_types = ['test_wngw', 'test_straight_wire', 'test_ic', 'test_snspd' ]
first_dev_loc = {'test_wngw':[0,0], 'test_straight_wire':[0,0], 'test_ic':[0,0], 'test_snspd':[0,0]}
num_die = 10
def get_start(num_die, typ):
    die_start = []
    for i in range(num_die):
        input('Move probe to first {typ} device start position and confirm [ENTER]'.format(typ = typ))
        startPt = sp.getPos()
        die_start += [startPt]
    return die_start
    
def measure(startPt, die_num, dev_type):
    for d in info:
        if 'has_info' in d and d['has_info'] is True and (d['type'] == dev_type): 
            loc = (np.array(d.midpoint) - np.array(first_dev_loc[dev_type]) + np.array(startPt))
            sp.moveAbs(loc[0],loc[1])
            sp.contact()
            res = k.get_R()
            d['actual_resistance {die-num}'.format(die_num = die_num)] = res
            sp.seperation()
    
for typ in dev_types:
    input('Adjust probes for {typ} and confirm [ENTER]'.formta(typ = typ))
    die_start = get_start(num_die, typ)
    for number, die in enumerate(die_start):
        measure(die,number, typ)
    
stream = open('WB_resistance.yaml','w')
yaml.dump(info,stream)
