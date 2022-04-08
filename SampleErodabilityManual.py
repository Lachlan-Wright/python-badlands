#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create regular grid and Sample Erodability raster data without a shapefile

Created on Fri Apr  8 11:46:52 2022

@author: lachlan_wright
"""
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import cmocean as cmo

# 1k grid across malawi region needs to be 381 x 717
nx = np.int32(380000/250) + 1
ny = np.int32(716000/250) + 1
# nx, ny = (381,717) # set number of XY cells (taken from badlands regrid)
xsample = np.linspace(0, 380000, nx) + 459132 # set up x axis and add UTM origin
ysample = np.linspace(0, 716000, ny) + 8338308 # set up y axis add URM origin

xx, yy = np.meshgrid(xsample,ysample)

coords2 = np.vstack((xx.flatten(), yy.flatten())).T

# open rasterio
src = rasterio.open('GeologyRaster/Geologyraster.tif')

Z = [x for x in src.sample(coords2)] # sample the dem across the grid
Z = np.concatenate( Z, axis=0 ) # concatonate arrays into one

# Plot to check
z = Z.reshape(2865,1521) # reshape into grid
plt.imshow(z,origin='lower', cmap = cmo.cm.thermal)
plt.clim(0, 10) # clip color limits
plt.colorbar(label = 'Elevation')

# Save Numpy array for remapping
np.save('GeologyRaster/Erodability.npy',z)