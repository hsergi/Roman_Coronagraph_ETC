#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
# For keep outs and to convert decimal dates into readable dates
import EXOSIMS, EXOSIMS.MissionSim
from astropy.time import Time
import astropy.units as u
# CSV output file
from scripts.store_csv_file import store_csv_file_acc

def cgi_etc_star_accessibility(CGI_epoch0, CGI_epoch1, jsonFile, 
    csvFileName, PName, hipPName):

    # EXOSIMS-CGI Perf prints out this message that clutters the session when running big loops:
    # EXOSIMS/EXOSIMS/OpticalSystem/Nemati_2019.py:422: RuntimeWarning: invalid value encountered in true_divide
    # Until it is addressed, I set off the warning temporarily
    np.seterr(divide='ignore', invalid='ignore')
    
    nPlanets = len(PName)
    # Write star names
    starName = [''] * nPlanets
    starNameCommon = [''] * nPlanets
    for i_p in np.arange(nPlanets):
        starName[i_p] = hipPName[i_p][0:len(hipPName[i_p])-2]    
        starNameCommon[i_p] = PName[i_p][0:len(PName[i_p])-2]
        
    # Deriving the accesible times for each target
    # Partly based on Dean Keithly's script "CalculateSpecificStarKeepOutMaps.py"
    # See that script for more details to get culprits for keep out areas. Or see also EXOSIMS/Prototypes/Observatory.py
    
    #Create Mission Object To Extract Some Plotting Limits
    # First time, it may take some time (60 stars~30 sec). Next times, the keepout file and other
    # results are cached
    #sim = EXOSIMS.MissionSim.MissionSim(jsonFile, nopar=True)
    sim = EXOSIMS.MissionSim.MissionSim(jsonFile, 
        # missionStart in MJD
        missionStart=Time(CGI_epoch0, format='byear').mjd,
        # missionLife in years
        missionLife=CGI_epoch1-CGI_epoch0)
    # 'KO' refers to Keep out
    obsKO, TLKO, TKKO = sim.Observatory, sim.TargetList, sim.TimeKeeping
    
    # Indices where the star is
    sIndsKO = np.empty(nPlanets, dtype=int)
    sIndsKO.fill(np.nan)
    for i_pl in np.arange(nPlanets):
        sIndsKO[i_pl] = np.where(TLKO.Name == starName[i_pl])[0]
    
    # Generate Keepout over Time (P.S. 'byear' may have 0.5 days error 
    # when translated into MJD, but 'decimalyear' prints out lots of warnngs 
    # from EFA library that are hard to slience and have to do with irrelevant 
    # leap second issues)
    koEvaltimes = np.arange(TKKO.missionStart.to_value('mjd'), \
        TKKO.missionStart.to_value('mjd') + \
        TKKO.missionLife.to('day').value, 1)
    # Cast them as Time type for the method keepout later on
    koEvaltimes = Time(koEvaltimes, format='mjd')
    
    # choose observing modes selected for detection (default marked with a flag)
    OS = TLKO.OpticalSystem
    allModes = OS.observingModes
    
    #Construct koangles
    nSystems  = 1 # All filters share the same keep out angle constraints. Alternative: len(allModes)
    systNames = np.unique([allModes[x]['syst']['name'] for x in np.arange(nSystems)])
    systOrder = np.argsort(systNames)
    koStr     = ["koAngles_Sun", "koAngles_Moon", "koAngles_Earth", "koAngles_Small"]
    koangles  = np.zeros([len(systNames),len(koStr),2])
    for x in systOrder:
        rel_mode = list(filter(lambda mode: mode['syst']['name'] == systNames[x], allModes))[0]
        koangles[x] = np.asarray([rel_mode['syst'][k] for k in koStr])
    # Printing out koangles (same for all filters)
    for idx in range(len(koStr)):
      print(f'{koStr[idx]:s}=[{koangles[0,idx,0]:.2f},{koangles[0,idx,1]:.2f}]')
    
    tmpkoGood, r_body, r_targ, tmpCulprit, koangleArray = \
        obsKO.keepout(TLKO, sIndsKO, koEvaltimes, koangles, True)
    koGood = np.squeeze(tmpkoGood[0]) # Since we are using the same angle constraints for each filter, we can just select the first one
    culprit = tmpCulprit[0]

    #creating an array of visibility based on culprit
    sunFault   = culprit[:,:,0]
    moonFault  = culprit[:,:,1]
    earthFault = culprit[:,:,2]
    mercFault  = culprit[:,:,3]
    venFault   = culprit[:,:,4]
    marsFault  = culprit[:,:,5]
    solarPanelFault  = culprit[:,:,11]
    
    print('Accessibility:')
    if nPlanets == 1:
        # For 1 planet the indices are different
        print(f'>> {starNameCommon[0]:s} ({starName[0]:s}): {np.sum(koGood)/len(koEvaltimes)*100:1.1f}% accessible')
    elif nPlanets > 1:
        for i_p in np.arange(nPlanets):
            print('%s (%s): %1.1f %% accessible (Inaccessible due to Solar Panels %1.1f, Sun %1.1f, Moon %1.1f, Earth %1.1f, Mercury %1.1f, Venus %1.1f, Mars %1.1f)' \
                      % (starNameCommon[i_p], starName[i_p],
                          np.sum(koGood[i_p]) / len(koEvaltimes) * 100, \
                          np.sum(solarPanelFault[i_p]) / len(koEvaltimes) * 100, \
                          np.sum(sunFault[i_p]) / len(koEvaltimes) * 100, \
                          np.sum(moonFault[i_p]) / len(koEvaltimes) * 100, \
                          np.sum(earthFault[i_p]) / len(koEvaltimes) * 100, \
                          np.sum(mercFault[i_p]) / len(koEvaltimes) * 100, \
                          np.sum(venFault[i_p]) / len(koEvaltimes) * 100, \
                          np.sum(marsFault[i_p]) / len(koEvaltimes) * 100))
    
    # Write CSV file with accessibility
    store_csv_file_acc(starNameCommon, koGood, len(koEvaltimes), CGI_epoch0, csvFileName)
    
    return koGood
