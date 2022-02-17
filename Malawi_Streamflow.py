#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to extract discharge data for Badlands Calibration

Created on Mon Jan 10 14:55:49 2022

@author: lachlan_wright
"""
import numpy as np


# get average flow values using getflow
S_Rukuru = get_flow(7085570)
Songwe = get_flow(7084413)
Ruhuhu = get_flow(7085317)
Bua = get_flow(7088187)
Dwangwa = get_flow(7087667)

rivers = np.array([[632142.5,8809728.2,S_Rukuru], # concatonate into array with xy coords
              [603033.3,8925928.9,Songwe],
              [672352.9,8835076.9,Ruhuhu],
              [637713.0,8585649.9,Bua],
              [627245.5,8835076.9,Dwangwa]])

np.savetxt('river_discharge.csv', rivers, delimiter = ',') # output to csv in X Y Discharge space