#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to sample the erodability raster from arcmap

Created on Sat Jan 15 13:30:05 2022

@author: lachlan_wright
"""
import rasterio
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Read points from shapefile
pts = gpd.read_file('Malawi_points/500mFishnet.shp')
pts.index = range(len(pts))
coords = [(x,y) for x, y in zip(pts.geometry.x, pts.geometry.y)]

# Open the raster and store metadata
src = rasterio.open('GeologyRaster/GeologyRaster.tif')

# Sample the raster at every point location and store values in DataFrame
pts['Raster Value'] = [x for x in src.sample(coords)]

# Check Extraction
# head = pts.head(5)
# print(head)

# format data for export
data = pd.DataFrame() # create empty data frame
data['X'] = pts['geometry'].x
data['Y'] = pts['geometry'].y
data['Erodability'] = pts['Raster Value']

# Sort values and remove square brackets
data = data.sort_values(['Y', 'X'], ascending=[True, True])
data['Erodability'] = data['Erodability'].str[0] # removes square brackets

# Plot data to check grid (taken from )
x = data['X']
y = data['Y']
erodability = data['Erodability']
dx = np.arange(min(x), max(x), 500)
dy = np.arange(min(y), max(y), 500)
X,Y = np.meshgrid(dx,dy)
Z = griddata((x,y), erodability, (X,Y), method = 'nearest')

fig = plt.figure(dpi = 300)
plt.imshow(Z,origin='lower') # flip figure axes
plt.colorbar(label = 'Rock Type')
plt.show()

# # Export to csv
# data['Erodability'].to_csv('Erodability500m.csv', header = False, index = False)

# Export to pickel
data.to_pickle('Erodability.pkl')