import ruamel.yaml
yaml = ruamel.yaml.YAML(typ='unsafe')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib 



stream = open('/home/linaro/nc-phidl/die/WB_info.yaml','r')
info = yaml.load(stream)

test_straight_wire = []
for dev in info:
    if dev['type']=='test_straight_wire':
     test_straight_wire += [dev]
data = {'expected_resistance':[],'wire_width':[],'length':[]}
for dev in test_straight_wire :
    for key in data:
        data[key] += [dev[key]]
plt.figure(1)   
plt.scatter(data['wire_width'],data['expected_resistance'])
plt.xlabel('Wire Width')
plt.ylabel('Expected Resistance')
plt.title('Test Straight Wire')

plt.figure(2)
plt.scatter(data['length'],data['expected_resistance'])
plt.xlabel('Length')
plt.ylabel('Expected Resistance')
plt.title('Test Straight Wire')

test_snpd=[]
for dev in info:
    if dev['type']=='test_snspd':
     test_snpd += [dev]
data2 = {'expected_resistance':[],'wire_width':[],'length':[],'num_squares':[]}
for dev in test_snpd :
    for key in data2:
        data2[key] += [dev[key]]
        
plt.figure(3)
plt.scatter(data2['num_squares'],data2['expected_resistance'])
plt.xlabel('Num Squares')
plt.ylabel('Expected Resistance')
plt.title('Test SNPD')

plt.figure(5)
norm=matplotlib.colors.LogNorm(vmin=min(data2['wire_width']), vmax=max(data2['wire_width']))
plt.scatter(data2['num_squares'],data2['expected_resistance'],norm=norm,c = data2['wire_width'])
cbar = plt.colorbar()
plt.title('Test SNPD')
plt.xlabel('Num Squares')
plt.ylabel('Expected Resistance')
cbar.set_label('Wire Width')
tic = list(set(data2['wire_width']))
cbar.set_ticks(tic)
cbar.set_ticklabels(tic)

plt.figure(6)
norm=matplotlib.colors.LogNorm(vmin=min(data2['wire_width']), vmax=max(data2['wire_width']))
plt.scatter(data2['length'],data2['expected_resistance'],norm = norm,c = data2['wire_width'])
cbar = plt.colorbar()
plt.xlabel('Length ($\mu m$)')
plt.ylabel('Expected Resistance ($k \Omega$)')
cbar.set_label('Wire Width ($\mu m$)')
tic = list(set(data2['wire_width']))
cbar.set_ticks(tic)
cbar.set_ticklabels(tic)
plt.title('Test SNPD')

test_wngw = []
for dev in info:
    if dev['type']=='test_wngw':
     test_wngw += [dev]
data3 = {'expected_resistance':[],'wire_width':[],'length':[],'num_squares':[]}
for dev in test_wngw:
    for key in data3:
        data3[key] += [dev[key]]
        
plt.figure(7)
norm=matplotlib.colors.LogNorm(vmin=min(data3['length']), vmax=max(data3['length']))
plt.scatter(data3['wire_width'],data3['expected_resistance'],norm=norm, c = data3['length'])
cbar = plt.colorbar()
tic = list(set(data3['length']))
cbar.set_ticks(tic)
cbar.set_ticklabels([int(round(i)) for i in tic])
plt.title('Test WNGW')
plt.xlabel('Width')
plt.ylabel('Expected Resistance')
cbar.set_label('Length')

plt.figure(8)
norm=matplotlib.colors.LogNorm(vmin=min(data3['wire_width']), vmax=max(data3['wire_width']))
plt.scatter(data3['num_squares'],data3['expected_resistance'],norm=norm, c = data3['wire_width'])
cbar = plt.colorbar()
tic = list(set(data3['wire_width']))
cbar.set_ticks(tic)
cbar.set_ticklabels(tic)
plt.title('Test WNGW')
plt.xlabel('Num Squares')
plt.ylabel('Expected Resistance')
cbar.set_label('Wire Width')