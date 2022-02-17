#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to remap Rocktype numbers to actual values

Created on Sun Jan 16 16:17:02 2022

@author: lachlan_wright
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import griddata

# Read in erodability data (from arcgis)
data = pd.read_excel('2k2022/Geology2k2022.xlsx', header=None, names = ['Erodability'])

# read in XY data (from arcgis)
coord = pd.read_csv('2k2022/2kgrid.dat', names = ['X', 'Y', 'Z'], header = 0, sep = ' ')

# Unpickle erodability data (if using python scripts)
#data = pd.read_pickle('Erodability.pkl')

# Plot data to check grid
x = coord['X']
y = coord['Y']
erodability = data['Erodability']
dx = np.arange(min(x), max(x), 2000)
dy = np.arange(min(y), max(y), 2000)
X,Y = np.meshgrid(dx,dy)
Z = griddata((x,y), erodability, (X,Y), method = 'nearest')

fig = plt.figure(dpi = 300)
plt.imshow(Z,origin='lower') # flip figure axes
plt.colorbar(label = 'Rock Type')
plt.show()

# Map rock numbers to erodability values
# Rock 1, 2, 3, 4, 5, 10 = 5e-7
# Rock 7, 8, 9 = 1e-7
data['Erodability'].replace(1.0, 5e-7, inplace = True)
data['Erodability'].replace(2.0, 5e-7, inplace = True)
data['Erodability'].replace(3.0, 5e-7, inplace = True)
data['Erodability'].replace(4.0, 5e-7, inplace = True)
data['Erodability'].replace(5.0, 5e-7, inplace = True)
data['Erodability'].replace(6.0, 5e-7, inplace = True) # changed from 6 to 6.0 
data['Erodability'].replace(7.0, 1e-7, inplace = True)
data['Erodability'].replace(8.0, 1e-7, inplace = True)
data['Erodability'].replace(9.0, 1e-7, inplace = True)
data['Erodability'].replace(10.0, 5e-7, inplace = True)

# Plot data to check mappings
Z = griddata((x,y), data['Erodability'], (X,Y), method = 'nearest')
fig = plt.figure(dpi = 300)
plt.imshow(Z,origin='lower') # flip figure axes
plt.colorbar(label = 'Rock Type')
plt.show()

# Export to csv
data['Erodability'].to_csv('Erodability2k.csv', header = False, index = False)