#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Global constant
from config import INSTALLATION_PATH
# Generic packages
import numpy as np
import hjson
import json
import os
from pathlib import Path
# For integration times
import astropy.units as u
# For keep outs and to convert decimal dates into readable dates
import EXOSIMS, EXOSIMS.MissionSim
from astropy.time import Time
# IMD (https://plandb.sioslab.com/index.php)
import pandas as pd
# (Optional) Plotting the results of reflected light exoplanets
import matplotlib.pyplot as plt
# Individual methods for each CI target
from scripts.cgi_etc_dust import cgi_etc_dust
from scripts.cgi_etc_sl import cgi_etc_sl
from scripts.cgi_etc_rv_shortest_integration_time import cgi_etc_rv_shortest_integration_time

# EXOSIMS/EXOSIMS/OpticalSystem/Nemati_2019.py:422: RuntimeWarning: invalid value encountered in true_divide
# I set off the warning temporarily
np.seterr(divide='ignore', invalid='ignore')

# Make a local copy
dir_cgi_etc = INSTALLATION_PATH
if dir_cgi_etc[-1] != '/':
    dir_cgi_etc += '/'

# json file (EXOSIMS)
jsonFile = dir_cgi_etc + 'json/cgi_etc_exosims.json'
# Make sure the file exists
if os.path.exists(jsonFile) == False:
    raise Exception("Copy json/cgi_etc_exosims_ref.json to " + \
        "json/cgi_etc_exosims.json (version for user's edits)")

# hjson file
hjsonFile = dir_cgi_etc + 'json/cgi_etc_setup.hjson'
# Make sure the file exists
if os.path.exists(hjsonFile) == False:
    raise Exception("Copy json/cgi_etc_setup_ref.hjson to " + \
        "json/cgi_etc_setup.hjson (version for user's edits)")

# Read parameters related to observations
with open(hjsonFile, 'r') as initIn:
        CGI_Observations = hjson.load(initIn)
        initIn.close()

# Type of CGI Target
CGI_targetType = CGI_Observations['targetType']
print(f'\n>> You are considering {CGI_targetType:s} observations\n')

# Check
if CGI_targetType.lower() != 'exo dust' and \
    CGI_targetType.lower() != 'self luminous' and \
    CGI_targetType.lower() != 'reflected light':
    
    raise Exception('>> Please choose either self luminous, exo dust, or ' + \
        'radial velocity for targetType in the setup file')

# Create the folder for output results
dir_out = dir_cgi_etc + 'output/'
if os.path.exists(dir_out) == False:
    os.mkdir(dir_out)
    
# Common parameters
CGI_epoch0 = CGI_Observations['CGI_epoch0']
CGI_epoch1 = CGI_Observations['CGI_epoch1']
filterList = CGI_Observations['filterList']
csvFileName = CGI_Observations['csvFileName']

if CGI_targetType.lower() == 'exo dust':
    cgi_etc_dust(CGI_epoch0, CGI_epoch1, filterList, jsonFile, \
    csvFileName, CGI_Observations[CGI_targetType]) 

if CGI_targetType.lower() == 'self luminous':
    cgi_etc_sl(CGI_epoch0, CGI_epoch1, filterList, jsonFile, \
    csvFileName, CGI_Observations[CGI_targetType])

if CGI_targetType.lower() == 'reflected light':
    cgi_etc_rv_shortest_integration_time(CGI_epoch0, CGI_epoch1, \
    filterList, jsonFile, csvFileName, CGI_Observations[CGI_targetType])

print('\n---------------------------------------')
print(' Estimated integration times written in: ' + \
    f"{dir_cgi_etc + 'output/csv/' + csvFileName + '.csv':s}")
print('---------------------------------------\n')
