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
from scripts.cgi_etc_star_accessibility import cgi_etc_star_accessibility
# Updated specs for EXOSIMS
from scripts.cgi_etc_update_specs import cgi_etc_update_specs
# CSV file
from scripts.store_csv_file import store_csv_file_ed
from scripts.store_csv_file import store_csv_file_rv
from scripts.store_csv_file import store_csv_file_sl
from scripts.store_csv_file import store_csv_file_acc
# Use to label the temporary json file
from datetime import datetime

print('>> All modules related to Roman Coronagraph ETC succesfully loaded')
print(f'>> The installation path in config.py is {INSTALLATION_PATH:s}')
