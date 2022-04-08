#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract a catchment from Badlands to calculate the average erosion
Created on Fri Apr  1 18:18:07 2022

@author: lachlan_wright
"""
import os
import h5py # import hdf5 reader
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cmocean as cmo

path = '/Users/lachlan_wright/Documents/PhD/Chapter3/Badlands/2022test/h5'
os.chdir(path)

# read hdf5 file
flow = h5py.File('flow.time25.hdf5', 'r')
tin = h5py.File('tin.time25.hdf5', 'r')
list(flow.keys()) # list the subsets in the file

# extract bits from hdf5 
tcoords = tin['/coords']
fcoords = flow['/coords']
basin = flow['/basin']
cumdiff = tin['/cumdiff']

# coordinates of tin
tx = tcoords[:,0]
ty = tcoords[:,1]

# coordinates of flow
fx = fcoords[:,0]
fy = fcoords[:,1]

# coordinates in catchment of intrest
x,y = [128385,402691]
x = np.int32((round(x,-3)/1000)+1) # convert to array dims
y = np.int32((round(y,-3)/1000)+1)

# varialbes of flow and tin
basin = basin[:,0]
cumdiff = cumdiff[:,0]

# number of points on the tin 
dx = 1000 # grid spacing
nx = np.int32(((max(tx)-min(tx))/dx)+1)
ny = np.int32(((max(ty)-min(ty))/dx)+1)

# xcoordinates
xsample = np.linspace(min(tx), max(tx), nx)
ysample = np.linspace(min(ty), max(ty), ny)

# resample onto tin
xx, yy = np.meshgrid(xsample,ysample)
basin = griddata((fx,fy), basin, (xx,yy), method = 'nearest')
cumdiff = griddata((tx,ty), cumdiff, (xx,yy), method = 'nearest')

# Extract basin number from coordiantes
catchID = basin[y,x]

#plot to check 
# fig = plt.figure(dpi = 300)
# plt.imshow(basin,origin='lower', alpha = 1) # flip figure axes
# plt.colorbar(label = 'basin #')
# plt.show()

# fig = plt.figure(dpi = 300)
# plt.imshow(basin,origin='lower', alpha = 1) # flip figure axes
# plt.colorbar(label = 'Erosion/Deposition (m)')
# plt.show()

# Extract data where mask is set
basin = np.ma.masked_not_equal(basin, catchID)
mask = np.ma.getmask(basin)
eroCatch = np.ma.array(cumdiff, mask=mask, fill_value = 0)

# get dimensions of array to subset
dims = np.asarray(basin.nonzero())
ymin = min(dims[0,:])
ymax = max(dims[0,:])
xmin = min(dims[1,:])
xmax = max(dims[1,:])

# Subset array
eroCatch = eroCatch[ymin:ymax, xmin:xmax]

# plot to check
fig = plt.figure(dpi = 300)
ax1 = fig.add_subplot(121)
ax1.set_title('Erosion/Deposition (m):')
ax1.plot()
plt.imshow(eroCatch, origin='lower', cmap = cmo.cm.balance) # flip figure axes
plt.clim(-100, 100) # clip color limits
plt.colorbar()

ax2 = fig.add_subplot(122)
ax2.set_title('Erosion (m):')
ax2.plot()
plt.imshow(eroCatch,origin='lower', cmap = cmo.cm.dense_r) # flip figure axes
plt.clim(0, -100) # clip color limits
plt.colorbar()

# replace de[position values with zero]
eroCatch = np.where(eroCatch < 0, eroCatch, 0)

# calculate volume
pixel_width = 1000
pixel_length = 1000
ras_con = 1;
width_con = 1;
length_con = 1;
eroCatchsum = np.sum(eroCatch)
eroCatchvol = abs((eroCatchsum*ras_con) * (pixel_width*width_con)
                  * (pixel_length*length_con))
print('Volume of eroded material = '+np.array2string(eroCatchvol)+' m3')
print('Volume of eroded material per year = '+np.array2string(eroCatchvol/140000)+' m3/a')
print('Average erosion rate = ' + np.array2string(abs(eroCatchsum/140000)) + ' m/a')

