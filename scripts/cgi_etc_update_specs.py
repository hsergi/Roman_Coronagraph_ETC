#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Global constant
from config import INSTALLATION_PATH
# Generic packages
import json, os
import numpy as np
from pathlib import Path
# For keep outs and to convert decimal dates into readable dates
import EXOSIMS
from astropy.time import Time
# Use to label the temporary json file
from datetime import datetime

def cgi_etc_update_specs(jsonFile, filter, CGI_epoch0, CGI_epoch1):

    # Keeping track of the actual value of the post-processing factor used in the estimations.
    # Notice that EXOSIMS's ppFact equals (1/kpp), where kpp is the post-processing factor in CGI Perf,
    # which is the usual way to report it. For instance, for the NF, kpp=2, and then EXOSIMS ppFact is 0.5.
    kpp_tmp = np.nan

    path = Path(jsonFile)
    with open(path) as ff:
        specs = json.loads(ff.read())
        ff.close()
    # Updating the instrumental specs because of the different post-processing factor for each filter.
    specs2 = specs
    # Values from CGI PS analysis (POC Marie Ygouf/JPL)
    if 'nf' in str.lower(filter):
        specs2['ppFact'] = 1/2.00 # Post-processing documentation available
    if 'amici' in str.lower(filter):
        specs2['ppFact'] = 1/1.22 # Preliminary results (02/23/21)
    if 'wf' in str.lower(filter):
        specs2['ppFact'] = 1/2.00 # Until there are OS simulations with these mode
    # Record the actual value of the ppFact used
    kpp_tmp = 1 / specs2['ppFact']
    # Writing temporary json file
    json_dir_tmp = INSTALLATION_PATH + 'json/tmp/'
    if os.path.exists(json_dir_tmp) == False:
        os.mkdir(json_dir_tmp)
    jsonFile_tmp = json_dir_tmp + 'cgi_etc_exosims_tmp_' + filter + '_' + \
        datetime.now().strftime('%m%d%y%H%M%S') + '.json'
    with open(jsonFile_tmp, "w") as ff_tmp:
        ff_tmp.write(json.dumps(specs2))
        ff_tmp.close()
    # We need to re-create the mission object because ppFact was changed
    simTmp = EXOSIMS.MissionSim.MissionSim(jsonFile_tmp,
        # missionStart in MJD
        missionStart=Time(CGI_epoch0, format='byear').mjd,
        # missionLife in years
        missionLife=CGI_epoch1-CGI_epoch0)
    # Remove temporary file
    os.remove(jsonFile_tmp)

    return kpp_tmp, simTmp.TargetList.OpticalSystem, simTmp.TargetList, simTmp.TimeKeeping
