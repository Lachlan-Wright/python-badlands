#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to sort displacement data into badlands format

Created on Fri Jan 14 21:10:30 2022

@author: lachlan_wright
"""
import pandas as pd

# read data from text
data = pd.read_csv('Displacement.cou',skiprows=3, sep = '\t', header = None)

# Subset into x y dz
data = data[[0, 1, 5]]

# Sort values and strip x y
data = data.sort_values([1, 0], ascending=[True, True])

data = data[[5]] # this just leaves the dz data in the file 
data = data.apply(lambda x: '%.5f' % x, axis=1) # removes scientific notation

# Export to csv
data.to_csv('displacements500m.dat', index = False, header = False)