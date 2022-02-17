#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function to pull streamflow data from the GEOGloWS ECMWF API

Created on Mon Jan 10 14:09:41 2022

@author: lachlan_wright
"""
def get_flow(reachID):
    
    import requests
    import numpy as np

    reach_id = str(reachID) # South Rukuru
    url ='https://geoglows.ecmwf.int/api/MonthlyAverages/?reach_id='+reach_id+'&return_format=json' # builds API url from known reach ID
        
    response = requests.get(url) # pull request
    response = response.json() # map to json format

    avgflow = np.average(np.array(response['time_series']['flow'])) #subset out the flow rates to numpy array and average

    print('The average flow in m3/s is:', avgflow)
    return(avgflow)