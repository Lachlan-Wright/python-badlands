#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to extract points from DEM for Badlands updated

Created on Fri Jan 14 14:59:13 2022

@author: lachlan_wright
"""

import rasterio
import geopandas as gpd
import pandas as pd

# Read points from shapefile
pts = gpd.read_file('Malawi_points/Etopo1_elevation_2.shp')
pts.index = range(len(pts))
coords = [(x,y) for x, y in zip(pts.geometry.x, pts.geometry.y)]

# Open the raster and store metadata
src = rasterio.open('DEMBathymetry_2022_2kres1.tif')

# Sample the raster at every point location and store values in DataFrame
pts['Raster Value'] = [x for x in src.sample(coords)]

# Check Extraction
#head = pts.head(5)
#print(head)

# format data for export
data = pd.DataFrame() # create empty data frame
data['X'] = pts['geometry'].x
data['Y'] = pts['geometry'].y
data['Z'] = pts['Raster Value']

# Sort values
data = data.sort_values(['Y', 'X'], ascending=[True, True])
data['Z'] = data['Z'].str[0] # remove brackets from list of 'Raster Values'

# Pickle data for use in Coordinate_Reduce.py
data.to_pickle('Elevation500m.pkl')

# Export to csv if not pickling for use later
# data.to_csv('Elevations500m.csv', header = False, index = False, sep = ' ')