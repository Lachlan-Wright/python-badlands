#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to plot coordinates
Created on Mon Jan 17 16:12:56 2022

@author: lachlan_wright
"""
import os
import h5py # import hdf5 reader
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import cmocean as cmo

path = '/Users/lachlan_wright/Documents/PhD/Chapter3/Badlands/lowstand_0.5precip/h5'
os.chdir(path)

f = h5py.File('tin.time10.hdf5', 'r') # read hdf5 file
list(f.keys())

coords = f['coords']
layDepth = f['layDepth']
layElv = f['layElev']
