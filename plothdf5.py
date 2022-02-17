#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to plot hdf5 files from bandlands

Created on Tue Jan 11 13:11:38 2022

@author: lachlan_wright
"""
import os
import h5py # import hdf5 reader
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cmocean as cmo

path = '/Users/lachlan_wright/Documents/PhD/Chapter3/Badlands/2022test2k/h5'
os.chdir(path)

f = h5py.File('tin.time0.hdf5', 'r') # read hdf5 file

# list(f.keys()) # list the subsets in the file

coords = f['coords'] # extract coordinates
# discharge = f['discharge'] # extract discharge values
lake = f['lake'] # extract lake values
# erodep = f['cumdiff'] # extract erodep values
# erodability = f['erodibility']
# chi = f['chi']

x = coords[:,0]
y = coords[:,1]
z = coords[:,2]

dx = np.arange(min(x), max(x), 500)
dy = np.arange(min(y), max(y), 500)

X,Y = np.meshgrid(dx,dy)

# discharge = discharge[:,0]
lake = lake[:,0]
# erodep = erodep[:,0]
# chi = chi[:,0]

Z = griddata((x,y), lake, (X,Y), method = 'nearest') # create grid

# Z = Z-456 # datum the topographic grid to lake level

### Plot figure
# fig = plt.figure(dpi = 300)
# plt.imshow(Z, cmap = cmo.cm.tarn_r,origin='lower') # flip figure axes
# plt.clim(-1000, 1000) # clip color limits
# plt.colorbar(label = 'topograpy (m)')
# plt.contour(Z, levels = [-600, -400, -200, 0], colors = 'black',
#             linestyles ='solid', linewidths = 0.5) # add contour lines to plot
# plt.show()

# fig = plt.figure(dpi = 300)
# plt.imshow(Z, cmap = cmo.cm.ice_r ,origin='lower') # flip figure axes
# plt.clim(0, 200000000) # clip color limits
# plt.colorbar(label = 'Discharge (m3/s)')
# plt.show()

# fig = plt.figure(dpi = 300)
# plt.imshow(Z, cmap = cmo.cm.balance ,origin='lower', alpha = 1) # flip figure axes
# plt.clim(-10, 10) # clip color limits
# # plt.imshow(Z, cmap = cmo.cm.ice ,origin='lower', alpha = 0.5) # flip figure axes
# # plt.clim(-10,0) # clip color limits
# plt.colorbar(label = 'EroDep (m)')
# # plt.contour(Z, levels = [10,50,100], colors = 'black',
#             # linestyles ='solid', linewidths = 0.5) # add contour lines to plot
# plt.show()

# fig = plt.figure(dpi = 300)
# plt.imshow(Z, cmap = cmo.cm.matter ,origin='lower') # flip figure axes
# plt.clim(0, 15) # clip color limits
# plt.colorbar(label = 'Chi')
# plt.show()

fig = plt.figure(dpi = 300)
plt.imshow(Z, cmap = cmo.cm.deep, origin='lower') # flip figure axes
plt.clim(0, 150) # clip color limits
plt.colorbar(label = 'Lake Depth (m)')
plt.contour(Z, levels = [10, 100], colors = 'black',
            linestyles ='solid', linewidths = 0.5) # add contour lines to plot
plt.show()