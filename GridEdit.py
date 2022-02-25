#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to manually correct topographic grid for badlands input

Created on Wed Feb 23 13:39:31 2022

@author: lachlan_wright

Define function to correct elevation values on line 72
"""
import matplotlib.pyplot as plt
from matplotlib.widgets import PolygonSelector
import matplotlib.path as mpltPath
import pandas as pd
import numpy as np
import cmocean as cmo

# read in elevation data using pandas
df = pd.read_csv('2K2022/2kgrid.dat', \
                 names = ['X', 'Y', 'Z'], header = 0, sep = ' ')

# reshape data to grid
z = df.values[:,2].reshape(359,191)

# Plot initial grid
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.set_title('polygon selection:')
ax1.plot()
ax1.set_xlim([0, 191])
ax1.set_ylim([0, 359])
plt.imshow(z,origin='lower',cmap = cmo.cm.tarn_r) # flip figure axes
plt.clim(468, 2000) # clip color limits
plt.colorbar(label = 'Elevation')

# Plot numpy array of zeros
array = np.zeros((359, 191))
ax2 = fig.add_subplot(122)
ax2.set_title('numpy array:')
msk = ax2.imshow(array, origin='lower', vmax=1, interpolation='nearest')
ax2.set_xlim([-2, 192])
ax2.set_ylim([-2, 360])

# Pixel coordinates
Xpix = np.arange(191)
Ypix = np.arange(359)
xv, yv = np.meshgrid(Xpix, Ypix)
pix = np.vstack((xv.flatten(), yv.flatten())).T

def updateArray(array, indices):
    lin = np.arange(array.size)
    newArray = array.flatten()
    newArray[lin[indices]] = 1
    return newArray.reshape(array.shape)

def onselect(verts):
    global array, pix
    p = mpltPath.Path(verts)
    ind = p.contains_points(pix, radius=1)
    array = updateArray(array, ind)
    msk.set_data(array)
    fig.canvas.draw_idle()

lasso = PolygonSelector(ax1, onselect)

plt.show(block = True)

# make bool mask from array
mask = array.astype(bool)

# define function to modify topography by
x = z[mask] # array of values within the mask
x = x[x<max(x)] # discard the maximum value (likely erroneous)
func = np.percentile(x,25) # take the lower percentile of datat

# Use where function to replace erroneus values
newz = np.where(mask, func, z)

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax1.set_title('original topography:')
ax1.plot()
ax1.set_xlim([0, 191])
ax1.set_ylim([0, 359])
plt.imshow(z,origin='lower', cmap = cmo.cm.tarn_r) # flip figure axes
plt.clim(468, 2000) # clip color limits
plt.colorbar(label = 'Elevation')

ax2 = fig.add_subplot(122)
ax2.set_title('new topography:')
ax2.plot()
ax2.set_xlim([0, 191])
ax2.set_ylim([0, 359])
plt.imshow(newz,origin='lower', cmap = cmo.cm.tarn_r) # flip figure axes
plt.clim(468, 2000) # clip color limits
plt.colorbar(label = 'Elevation')

# reshape data to original format using ravel and append to dataframe
newz = np.ravel(newz)
df['Z'] = newz

# write elevation data out to text
df.to_csv('2K2022/2kgridEdit.dat', header = False, index = False, sep = ' ')

# write mask out for later use
np.save('2K2022/mask', mask)