#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create regular grid and Sample DEM data without a shapefile

Created on Tue Mar  1 11:48:20 2022

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
src = rasterio.open('Dem2022/SRTM_BATHY_Lyons2022-001.tif')

Z = [x for x in src.sample(coords2)] # sample the dem across the grid
Z = np.concatenate( Z, axis=0 ) # concatonate arrays into one

# Datum to sealevel
Z = Z - 468
# Plot to check
z = Z.reshape(2865,1521) # reshape into grid
plt.imshow(z,origin='lower', cmap = cmo.cm.tarn_r)
plt.clim(0, 2000) # clip color limits
plt.colorbar(label = 'Elevation')

# create grid with elevations
x = np.linspace(0, 380000, nx) # x coordinates
y = np.linspace(0, 716000, ny) # y coordinates
xx, yy = np.meshgrid(x,y) # create mesh
grid = np.vstack((xx.flatten(), yy.flatten())).T #flatten into badlands format
grid = np.insert(grid, 2, Z, axis=1) # using np to insert elevation data

# export as csv with 2dp precision
np.savetxt("nodes.dat", grid, delimiter=" ", fmt="%.2f")