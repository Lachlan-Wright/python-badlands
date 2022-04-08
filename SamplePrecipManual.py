#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to extract precipiration data for badlands

Created on Tue Mar 22 10:41:32 2022

@author: lachlan_wright
"""
import numpy as np
import matplotlib.pyplot as plt
import rasterio
import cmocean as cmo
from scipy.ndimage import gaussian_filter

# 1k grid across malawi region needs to be 381 x 717
nx, ny = (1521,2865) # set number of XY cells (taken from badlands regrid)
xsample = np.linspace(0, 380000, nx) + 459132 # set up x axis and add UTM origin
ysample = np.linspace(0, 716000, ny) + 8338308 # set up y axis add URM origin

xx, yy = np.meshgrid(xsample,ysample)

coords2 = np.vstack((xx.flatten(), yy.flatten())).T

# open precip data (note in mm/month)
src = rasterio.open('Precip2022/MalawiPrecipUTM.tif')

Z = [x for x in src.sample(coords2)] # sample the dem across the grid
Z = np.concatenate( Z, axis=0 ) # concatonate arrays into one
z = Z.reshape(2865,1521) # reshape into grid

# smooth with gaussian filter
z = gaussian_filter(z, sigma=30)

# convert mm/month into m/a
z = z*(12/1000)

# create a series of scaled precipitation maps for BADLANDS input
# scalings taken from lyons et al., 2011 hydrologic balance
z550 = z*0.45 #550 m lowstand
z350 = z*0.53 #350 m lowstand
z200 = z*0.58 #200 m lowstand
z100 = z*0.63 # 100m lowstand
zsc = z*0.90 

# import watershed and alke outlines from numpy
pts = np.load('Watershed/watershed.npy')/250
pts2 = np.load('Watershed/lakeshore.npy')/250

# plot to check
plt.imshow(zsc,origin='lower', cmap = cmo.cm.rain)
plt.clim(0, 3) # clip color limits
plt.plot(pts[0], pts[1],'k--',linewidth=0.5)
plt.colorbar(label = 'Precipitation (m/a)')
plt.show()

plt.imshow(z100,origin='lower', cmap = cmo.cm.rain)
plt.clim(0, 3) # clip color limits
plt.plot(pts[0], pts[1],'k--',linewidth=0.5)
plt.colorbar(label = 'Precipitation (m/a)')
plt.show()

plt.imshow(z200,origin='lower', cmap = cmo.cm.rain)
plt.clim(0, 3) 
plt.plot(pts[0], pts[1],'k--',linewidth=0.5)
plt.colorbar(label = 'Precipitation (m/a)')
plt.show()

plt.imshow(z350,origin='lower', cmap = cmo.cm.rain)
plt.clim(0, 3) # clip color limits
plt.plot(pts[0], pts[1],'k--',linewidth=0.5)
plt.colorbar(label = 'Precipitation (m/a)')
plt.show()

plt.imshow(z550,origin='lower', cmap = cmo.cm.rain)
plt.clim(0, 3) # clip color limits
plt.plot(pts[0], pts[1],'k--',linewidth=0.5)
plt.colorbar(label = 'Precipitation (m/a)')
plt.show()

# reshape data to original format using ravel and export
zsc = np.ravel(zsc)
z100 = np.ravel(z100)
z200 = np.ravel(z200)
z350 = np.ravel(z350)
z550 = np.ravel(z550)

np.savetxt('Precip2022/precipScaled.csv', zsc, fmt='%f')
np.savetxt('Precip2022/precip100.csv', z100, fmt='%f')
np.savetxt('Precip2022/precip200.csv', z200, fmt='%f')
np.savetxt('Precip2022/precip350.csv', z350, fmt='%f')
np.savetxt('Precip2022/precip550.csv', z550, fmt='%f')