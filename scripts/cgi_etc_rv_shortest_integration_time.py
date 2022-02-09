#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generic packages
import numpy as np
import hjson, json, os
from pathlib import Path
# For integration times
import astropy.units as u
# For keep outs and to convert decimal dates into readable dates
import EXOSIMS, EXOSIMS.MissionSim
from astropy.time import Time
from scripts.cgi_etc_star_accessibility import cgi_etc_star_accessibility
# (Optional) Plotting the results
import matplotlib.pyplot as plt
# IMD
import pandas as pd 
# Updated specs for EXOSIMS
from scripts.cgi_etc_update_specs import cgi_etc_update_specs
# Linear interpolation
from scipy import interpolate
# CSV file
from scripts.store_csv_file import store_csv_file_rv

def cgi_etc_rv_shortest_integration_time(CGI_epoch0, CGI_epoch1, filterList, jsonFile, csvFileName, CGI_Observations):

    # Path with the orbital data of the planets from IMD (https://plandb.sioslab.com/index.php)
    pathIMD = './imd/'
    # Meaning of table parameters from IMD (# https://plandb.sioslab.com/docs/html/index.html#planetorbits-table)
    # t = time in days since 01/01/2026
    # r = actual distance planet-host star in AU
    # s = visual sepraration
    # beta = orbital phase angle
    
    # Remember (See above) that IMD data start at 01/01/2026 (not sure whether it is based on mJD, ISO, or else)
    imdEpoch0 = 2026.00
    
    # P.S. PName is used later on to read csv files from IMD
    # P.P.S. Leave a blank space between the name of the star and the planet, e.g., 14 Her b
    PName = CGI_Observations['PName']
    nPlanets = len(PName)
    # HIP identifiers
    hipPName = CGI_Observations['hipPName']

    # Derive the star's accessibility
    accessibleDays = cgi_etc_star_accessibility(CGI_epoch0, CGI_epoch1,
        jsonFile, csvFileName, PName, hipPName)
   
    # Write star names
    starName = [''] * nPlanets
    starNameCommon = [''] * nPlanets
    for i_p in np.arange(nPlanets):
        starName[i_p] = hipPName[i_p][0:len(hipPName[i_p])-2]    
        starNameCommon[i_p] = PName[i_p][0:len(PName[i_p])-2]
    
    # Values of the cloud fsed used by IMD
    cloudFsed = [0.00, 0.01, 0.03, 0.10, 0.30, 1.00, 3.00, 6.00]
    nFsed = len(cloudFsed)
    # Table of weights used to average the DMag from IMD (table provided by Mark Marley to Vanessa Bailey)
    freqFsed = [0.099, 0.001, 0.005, 0.010, 0.025, 0.280, 0.300, 0.280]
    # Make sur eit is normalized (it is, just if it gets changed in the future)
    freqFsed = freqFsed / np.sum(freqFsed)
    
    # Filters: Band 1, 3 and 4
    # P.S. Technical note for developers: Use 'NF', 'Amici_Spec' and 'WF', respectively, because 
    # these substrings are used when assigning the actual value of 
    # the post-processing value for each mode. Also, EXOSIMS makes use of 'Amici' and 'Spec' in Nemati_2019.py
    nFilters = len(filterList)
    # Keeping track of the actual value of the post-processing factor used in the estimations.
    # Notice that EXOSIMS's ppFact equals (1/kpp), where kpp is the post-processing factor in CGI Perf, 
    # which is the usual way to report it. For instance, for the NF, kpp=2, and then EXOSIMS ppFact is 0.5.
    kppList = np.empty(nFilters)
    kppList.fill(np.nan)
    
    ####################################################
    # Deriving expected integration times given an SNR #
    ####################################################
    
    # SNR list
    SNRRefList = CGI_Observations['SNRList']
    nSNRRef = len(SNRRefList)
    # SNR list to derive the integration times (fast, no worries)
    # Grid of values of SNR, instead of results for the values in SNRRefList only.
    # P.S. Small SNR values are used to highlight cases that are not worth
    # observing
    SNRList = np.sort(np.concatenate([SNRRefList, np.arange(0.5,20,0.5),
        np.arange(20,105,5)], axis=0))
    nSNR = len(SNRList)
    # Keeping track of the SNR actually found (in general, it should be the same as 
    # in SNRRefList but they are the values in SNRList closest to SNRRefList)
    SNRRefFound = np.empty(len(SNRRefList))
    SNRRefFound.fill(np.nan)
    
    ## First and last indices for the epochs under consideration
    dayEpoch0 = np.round(365.25 * (CGI_epoch0 - imdEpoch0)).astype(int)
    dayEpoch1 = np.round(365.25 * (CGI_epoch1 - imdEpoch0)).astype(int)
    # Imaging Mission Database says that the orbits are computed every 30 days, but there are cases where this is not the case (02/10/21: https://plandb.sioslab.com/plandetail.php?name=47+UMa+d whose CSV table has steps of 141 days)
    # I just assume it is 1 day, although in general it is larger. No problem. The rest of unused indices are filled with NaN

    dayEpochArray = np.empty((nPlanets, dayEpoch1 - dayEpoch0 + 1))
    dayEpochArray.fill(np.nan)
    waArcsecArray = np.empty((nPlanets, dayEpoch1 - dayEpoch0 + 1))
    waArcsecArray.fill(np.nan)
    fRatioArray = np.empty((nPlanets, nFilters, dayEpoch1 - dayEpoch0 + 1))
    fRatioArray.fill(np.nan)
    intTimeFilterHours = np.empty((nPlanets, nFilters, nSNR, dayEpoch1 - dayEpoch0 + 1))
    intTimeFilterHours.fill(np.nan)
    sInds = np.empty(nPlanets, dtype=int)
    sInds.fill(np.nan)
    
    # Looping over filters
    for i_flt in np.arange(nFilters):
    # Updating the instrumental specs because of the different post-processing factor for each filter.
        kppTmp, OSTmp, TLTmp, TKTmp = \
        cgi_etc_update_specs(jsonFile, filterList[i_flt],
            CGI_epoch0, CGI_epoch1)
        kppList[i_flt] = kppTmp
        mode = list(filter(lambda mode: mode['instName'] == filterList[i_flt], OSTmp.observingModes))[0]
        # Local zodi
        fZ = TLTmp.ZodiacalLight.fZ0
        # Loop over planets
        for i_pl in np.arange(nPlanets):
            # Index where the host star is found in the target list
            sInds[i_pl] = np.where(TLTmp.Name == starName[i_pl])[0]
            # Reading the CSV file from IMD
            PStr = PName[i_pl]
            # P.S. From IMD: if no inclination available, orbit is assumed edge-on. If no eccentricity is available, orbit is assumed circular. 
            planetDataOrig = pd.read_csv(pathIMD + PStr.replace(' ', '_' ) + '_orbit_data.csv')
            # IMD documentation (point 11 in https://plandb.sioslab.com/docs/html/index.html#planetorbits-table)
            # say (sic) "NaN when period of time of periastron passage are undefined"
            # If this is the case skip the planet
            if np.isnan(planetDataOrig['t']).all() == True:
                print('WARNING: Planet ' + PName[i_pl] + ' has undefined Ephemeris. Skipping it ...')
                continue
            # Creating a new pandas dataframe for each day using linear interpolation
            dict_tmp = {}
            dict_tmp['t'] = dayEpoch0 + np.arange(dayEpoch1-dayEpoch0+1)
            for column in planetDataOrig.columns:
                if column == 't': continue
                if isinstance(planetDataOrig[column][0], float):
                    interpolant = interpolate.interp1d(planetDataOrig['t'],
                        planetDataOrig[column], kind='linear')
                    dict_tmp[column] = interpolant(dict_tmp['t'])
            # database
            planetDataCgi = pd.DataFrame.from_dict(dict_tmp)
            dayEpochArray[i_pl,0:len(planetDataCgi)] = planetDataCgi['t']
            # Angular visual separation of the planet
            waArcsec = planetDataCgi['WA'].values / 1000 * u.arcsec
            waArcsecArray[i_pl,0:len(waArcsec)]=waArcsec.value
            # Actual planet-star distance (only used for exozodi)
            r_au = planetDataCgi['r'].values * u.AU
            # Fiducial visual inclination (only used for exozodi). The CSV files from IMD do not provide it.
            inc_deg = [20] * u.deg
            # Exozodi along the orbit
            fEZ = TLTmp.ZodiacalLight.fEZ(np.array([TLTmp.MV[sInds[i_pl]]]), inc_deg, r_au)
            fRatio = np.zeros(len(planetDataCgi['t']))
            # Looping over cloud fsed to get the average flux ratio
            for i_fsed in np.arange(nFsed):
                # Using the center wavelength of each observing mode to select the corresponding data
                # These values are stored in new columns pPhi_XXXC_YYYNM and dMag_XXXC_YYYNM 
                # where XXX is the cloud fsed scaled by 100 (000 representing no cloud) and 
                # YYY is the wavelength in nm.
                keyPlanetDataCgi = 'dMag_' + str(format(np.round(cloudFsed[i_fsed] * 100).astype(int),'03d')) + 'C_' + str(mode['lam'].to_value().astype(int)) + 'NM'
                fRatio = fRatio + freqFsed[i_fsed] * np.power(10,-0.4 * planetDataCgi[keyPlanetDataCgi])
    
            fRatioArray[i_pl, i_flt,0:len(fRatio)]= np.array(fRatio)
            dMags = -2.5 * np.log10(np.array(fRatio))
            # Only consider days that are accessible
            try:
                dMags[accessibleDays==False]=np.nan
            # Pass in case accessibility has not been computed
            except:
                pass
            # Looping over SNR
            for i_snr in np.arange(nSNR):
                mode['SNR'] = SNRList[i_snr]
                intTimeTmp = OSTmp.calc_intTime(TLTmp, np.array([sInds[i_pl]]), fZ, fEZ, dMags, waArcsec, mode, TK=TKTmp).to('hour').value
                intTimeTmp[np.where(intTimeTmp == 0)] = np.nan
                intTimeFilterHours[i_pl, i_flt, i_snr, 0:len(fRatio)] = intTimeTmp
                
    # Restoring the 'true_divide' error after EXOSIMS run
    np.seterr(divide='warn', invalid='warn')

        # Getting the maximum time that the target is accessible and its SNR
    SNRPlanetMax = np.empty((nPlanets, nFilters))
    SNRPlanetMax.fill(np.min(SNRList))
    intTimeSNRMax = np.empty((nPlanets, nFilters))
    intTimeSNRMax.fill(np.nan)
    intTmpHours = np.empty((nSNR))
    intTmpHours.fill(np.nan)
    for i_pl in np.arange(nPlanets):
        # Days that the target is accessible
        if nPlanets == 1:
           nDaysPlanet = np.sum(accessibleDays)
        else:
           nDaysPlanet = np.sum(accessibleDays[i_pl])
        for i_flt in np.arange(nFilters):
           for i_snr in np.arange(nSNR):
               # Shortest integration time within accessible times
               intTmpHours[i_snr] = \
                   np.nanmin(intTimeFilterHours[i_pl, i_flt, i_snr, :])
               # First time that it is not possible to achieve an SNR,
               # it means that the previous step was the largest value
               if np.isnan(intTmpHours[i_snr]) == False:
                   # If the integration time fits within the accessibility window
                   if intTmpHours[i_snr] <= (nDaysPlanet*24):
                       SNRPlanetMax[i_pl, i_flt] = SNRList[i_snr]
                       intTimeSNRMax[i_pl, i_flt] = intTmpHours[i_snr]
                   else:
                       SNRInterpolant = interpolate.interp1d(
                           intTmpHours[0:i_snr+1], SNRList[0:i_snr+1],
                           kind='linear')
                       # Round to 1 decimal place (it's SNR)
                       SNRPlanetMax[i_pl, i_flt] = \
                           np.round(SNRInterpolant(nDaysPlanet*24), decimals=1)
                       intTimeSNRMax[i_pl, i_flt] = nDaysPlanet*24

    # Replace bad cases by NaN now
    for i_pl in np.arange(nPlanets):
        for i_flt in np.arange(nFilters):
            if SNRPlanetMax[i_pl, i_flt] == np.min(SNRList):
                SNRPlanetMax[i_pl, i_flt] = np.nan
                intTimeSNRMax[i_pl, i_flt]= np.nan
    
    # Summarize results
    nSNRRef = len(SNRRefList)
    # The Epoch of observation, WA, and flux ratio do not change with SNR
    dayEpochBestTime = np.empty((nPlanets, nFilters, nSNR, 3))
    dayEpochBestTime.fill(np.nan)
    # Days that are necessary to get the integration time 
    # (e.g., according to some observing sequence, like OS11)
    dayOperationalBestTime = np.empty((nPlanets, nFilters, nSNR, 3))
    dayOperationalBestTime.fill(np.nan)
    # In the case of OS11, we have that 14 hours out of 24 are dedicated to observing a target
    fOperation = 14 / 24 ; 
    waMasBestTime = np.empty((nPlanets, nFilters, nSNR, 3))
    waMasBestTime.fill(np.nan)
    fRatioBestTime = np.empty((nPlanets, nFilters, nSNR, 3))
    fRatioBestTime.fill(np.nan)
    # The integration time depends on the SNR
    intTimeBestHours = np.empty((nPlanets, nFilters, nSNR))
    intTimeBestHours.fill(np.nan)
    
    for i_pl in np.arange(nPlanets):
        for i_flt in np.arange(nFilters):
            i_snr_2 = 0
            for snr in SNRRefList:
                i_snr = int(np.where(np.abs(snr - SNRList) == \
                    np.min(np.abs(snr - SNRList)))[0][0])
                # Finding the shortest integration time
                # If all are NaN, skip
                if (np.isnan(intTimeFilterHours[i_pl, i_flt, i_snr]).all()) == True:
                    continue
                indBest = np.where(intTimeFilterHours[i_pl, i_flt, i_snr] == np.nanmin(intTimeFilterHours[i_pl, i_flt, i_snr]))
                # Veerify that the integration time is less than the maximum available
                if (indBest[0].size != 0) and \
                    (intTimeFilterHours[i_pl, i_flt, i_snr, indBest] < intTimeSNRMax[i_pl, i_flt]):
                    dayEpochBestTime[i_pl, i_flt, i_snr_2, 1] = dayEpochArray[i_pl, indBest]
                    dayOperationalBestTime[i_pl, i_flt, i_snr_2, 1] = dayEpochArray[i_pl, indBest]
                    waMasBestTime[i_pl, i_flt, i_snr_2, 1] = waArcsecArray[i_pl, indBest] * 1000 # arcsec to milli-arcsec
                    fRatioBestTime[i_pl, i_flt, i_snr_2, 1] = fRatioArray[i_pl, i_flt, indBest]
                    intTimeBestHours[i_pl, i_flt, i_snr_2] = intTimeFilterHours[i_pl, i_flt, i_snr, indBest]
                    # Filling out the values before/after the best time
                    dayEpochBestTime[i_pl, i_flt, i_snr_2, 0] = dayEpochBestTime[i_pl, i_flt, i_snr, 1] - intTimeBestHours[i_pl, i_flt, i_snr] / 24 / 2
                    # In case the first date is before the mission start
                    if dayEpochBestTime[i_pl, i_flt, i_snr_2, 0] < 0:
                        dayEpochBestTime[i_pl, i_flt, i_snr_2, 0] = 0
                        dayEpochBestTime[i_pl, i_flt, i_snr_2, 2] = dayEpochBestTime[i_pl, i_flt, i_snr_2, 1] + intTimeBestHours[i_pl, i_flt, i_snr_2] / 24
                    else:
                        dayEpochBestTime[i_pl, i_flt, i_snr_2, 2] = dayEpochBestTime[i_pl, i_flt, i_snr_2, 1] + intTimeBestHours[i_pl, i_flt, i_snr_2] / 24 / 2
                    # Operational days have a fudge factor
                    dayOperationalBestTime[i_pl, i_flt, i_snr_2, 0] = dayEpochBestTime[i_pl, i_flt, i_snr_2, 1] - ( 1 / fOperation) * intTimeBestHours[i_pl, i_flt, i_snr_2] / 24 / 2
                    # In case the first date is before the mission start
                    if dayOperationalBestTime[i_pl, i_flt, i_snr_2, 0] < 0:
                        dayOperationalBestTime[i_pl, i_flt, i_snr_2, 0] = 0
                        dayOperationalBestTime[i_pl, i_flt, i_snr_2, 2] = dayEpochBestTime[i_pl, i_flt, i_snr_2, 1] + ( 1 / fOperation ) * intTimeBestHours[i_pl, i_flt, i_snr_2] / 24
                    else:
                        dayOperationalBestTime[i_pl, i_flt, i_snr_2, 2] = dayEpochBestTime[i_pl, i_flt, i_snr_2, 1] + ( 1 / fOperation ) * intTimeBestHours[i_pl, i_flt, i_snr_2] / 24 / 2
                    
                    waMasBestTime[i_pl, i_flt, i_snr_2, 0] = np.interp(dayEpochBestTime[i_pl, i_flt, i_snr_2, 0], 
                                                              dayEpochArray[i_pl,~np.isnan(dayEpochArray[i_pl])], 
                                                              1000 * waArcsecArray[i_pl,~np.isnan(dayEpochArray[i_pl])])
                    waMasBestTime[i_pl, i_flt, i_snr_2, 2] = np.interp(dayEpochBestTime[i_pl, i_flt, i_snr_2, 2], 
                                                              dayEpochArray[i_pl,~np.isnan(dayEpochArray[i_pl])], 
                                                              1000 * waArcsecArray[i_pl,~np.isnan(dayEpochArray[i_pl])])
                    fRatioBestTime[i_pl, i_flt, i_snr_2, 0] = np.interp(dayEpochBestTime[i_pl, i_flt, i_snr_2, 0], 
                                                              dayEpochArray[i_pl,~np.isnan(dayEpochArray[i_pl])], 
                                                              fRatioArray[i_pl, i_flt, ~np.isnan(dayEpochArray[i_pl])])
                    fRatioBestTime[i_pl, i_flt, i_snr_2, 2] = np.interp(dayEpochBestTime[i_pl, i_flt, i_snr_2, 2], 
                                                              dayEpochArray[i_pl, ~np.isnan(dayEpochArray[i_pl])], 
                                                              fRatioArray[i_pl, i_flt, ~np.isnan(dayEpochArray[i_pl])])
                # Update counter of SNR provided by the user
                i_snr_2 += 1    

    # Maximum integration times in hours (used for plotting)
    maxIntTimeHours = CGI_Observations['maxIntTimeHours'] # maximum CI allocation time for a single target
    
    # Create the folder where the figures will be stored
    dir_figures = './output/figures/'
    if os.path.exists(dir_figures) == False:
        os.mkdir(dir_figures)
    
    # Selecting the planets with some integration time
    indPlanetOK = np.empty(0, dtype=int)
    indPlanetOK.fill(np.nan)
    # Sentinel
    i_pl_OK = 0
    for i_pl in np.arange(nPlanets):
        if np.isnan(intTimeFilterHours[i_pl]).all() == False:
            indPlanetOK = np.append( indPlanetOK, i_pl_OK )
            i_pl_OK += 1
    # Number of planets with some finite integration times.
    nPlanetOK = len(indPlanetOK)

    ###################################
    # Store the results in a CVS file #
    ###################################
    store_csv_file_rv(filterList, kppList, PName,
        dayEpochBestTime, waMasBestTime, fRatioBestTime,
        SNRRefList, intTimeBestHours, SNRPlanetMax,
        intTimeSNRMax, csvFileName)
    
    ###############################################
    # Plotting the results for the most favorable #
    # time without taking into account the        #
    # accessibility of each target                #
    ###############################################

    # Useful to extract elements from a list (https://code.activestate.com/recipes/577953-get-multiple-elements-from-a-list/)
    getVar = lambda searchList, ind: [searchList[i] for i in ind]

    # Turn off to stop plotting the results 
    # 10/28/21: coming soon
    if CGI_Observations['bar_plot'].lower() == 'yes':
        # Font size
        fontSize = 18
        # Number of planets per plot
        nPlanetPlot = np.min([6,nPlanetOK]) 
        # Number of plots
        nPlots = np.ceil(nPlanetOK / nPlanetPlot)
        # Horizontal bar plot following https://stackoverflow.com/questions/9626298/matplotlib-chart-creating-horizontal-bar-chart
        # Colors
        colors_list = ['blue', 'tab:cyan', 'darkgreen', 'mediumseagreen', 'red', 'coral' ]
        # Alpha channel
        alphaChannelSNR = (1 / nSNRRef) * (nSNRRef - np.arange(nSNRRef))
        # Width of the bar
        width_bar = 1
        # Width of the space between bars
        width_space = 0.5
        #some calculation to determine the position of Y ticks labels
        total_space = nPlanetPlot * (nFilters * width_bar) + (nPlanetPlot - 1) * width_space
        ind_space = nFilters * width_bar
        step = ind_space / 2.
        pos = np.arange(step, total_space + width_space, ind_space + width_space)
        # Showing grid lines behind the bar figure (https://stackoverflow.com/questions/1726391/matplotlib-draw-grid-lines-behind-other-graph-elements)
        plt.rc('axes', axisbelow=True)
        # Properties for the text on the bars
        fontText = {'family': 'Arial',
                'color':  'black',
                'weight': 'bold',
                'size': 15
                }
        # Sentinel to add the text on the plot
        # This kludge will work if the filters are ordered as EB, DRM, EB, DRM,...
        # Otherwise, no big deal, the information will be added to each bar
        txtFlt = np.empty(nFilters, dtype=int)
        txtFlt.fill(1)
        for i_flt in np.arange(nFilters-1):
            if (filterList[i_flt][3:] == filterList[i_flt+1][4:]):
                txtFlt[i_flt]=0
            
        # Looping over plots
        for i_plt in np.arange(nPlots, dtype='int'):
            fig = plt.figure(figsize=(15,3 * nPlanetPlot))
            ax = fig.add_axes([0.05, 0.05, 0.8, 0.9])
            indPlanet1 = int(i_plt * nPlanetPlot)
            indPlanet2 = int(indPlanet1 + nPlanetPlot)
            if indPlanet2 > nPlanetOK:
                indPlanet2 = nPlanetOK
            indPlanetOK2 = indPlanetOK[indPlanet1:indPlanet2]
            PNamePlot = getVar(PName, indPlanetOK2)
            if indPlanet2 == nPlanetOK:
                for i_tmp in np.arange(int(indPlanet1 + nPlanetPlot) - nPlanetOK):
                    PNamePlot += ['']
            # Loop over planets
            for i_pl in np.arange(indPlanet2 - indPlanet1, dtype=int):
                # Actual index for the planet
                i_pl_true = indPlanetOK[i_pl + indPlanet1]
                for i_flt in np.arange(nFilters):
                    for i_snr in np.arange(nSNRRef-1,-1,-1):
                        indxSNR = int(np.where(np.abs(SNRRefList[i_snr] - SNRList) == \
                                               np.min(np.abs(SNRRefList[i_snr] - SNRList)))[0][0])
                        dataPlot = np.log10(intTimeBestHours[i_pl_true, i_flt, indxSNR])
                        if (i_pl == 0) and (i_snr == 0):
                            ax.barh(pos[i_pl] - step + i_flt * width_bar, dataPlot, width_bar, 
                                    facecolor=colors_list[i_flt], edgecolor='k', linewidth=3,
                                    label= '%s ($k_{pp}$=%1.2f)' % (filterList[i_flt], kppList[i_flt]))
                        else:
                            ax.barh(pos[i_pl] - step + i_flt * width_bar, dataPlot, width_bar, 
                                    facecolor=colors_list[i_flt], edgecolor='k', linewidth=3, alpha=alphaChannelSNR[i_snr])
                        if SNRRefList[i_snr] == np.min(SNRRefList):
                            if (~np.isnan(dataPlot)):
                                # Determining whether the integration time is within one of the accesible windows for the target
                                dayOpsStartTmp = int(np.round(dayOperationalBestTime[i_pl_true, i_flt, indxSNR, 0]))
                                dayOpsEndTmp = int(np.round(dayOperationalBestTime[i_pl_true, i_flt, indxSNR, 2]))
                                # Start and end days as if one could just integrate on the target, i.e, without other operations, like observing the reference star, etc
                                dayEpochStartTmp = int(np.round(dayOperationalBestTime[i_pl_true, i_flt, indxSNR, 0]))
                                dayEpochEndTmp = int(np.round(dayOperationalBestTime[i_pl_true, i_flt, indxSNR, 2]))
                                if np.sum(koGood[i_pl_true][dayOpsStartTmp:dayOpsEndTmp]) == (dayOpsEndTmp - dayOpsStartTmp):
                                    accessibilityOpsPlanetTmp = 'YES'
                                else:
                                    accessibilityOpsPlanetTmp = 'NO'
                                if np.sum(koGood[i_pl_true][dayEpochStartTmp:dayEpochEndTmp]) == (dayEpochEndTmp - dayEpochStartTmp):
                                    accessibilityEpochPlanetTmp = 'YES'
                                else:
                                    accessibilityEpochPlanetTmp = 'NO'
                                    
                                if (txtFlt[i_flt]):
                                    textString = 'Access Ops:%s, Obs:%s, DayOps$_0$=%1.1f, $\\Delta$DayOps=%1.1f, ' \
                                    '$\\Delta$DayObs=%1.1f, WA=%1.1f-%1.1f mas, FR=%1.1e-%1.1e' \
                                    % (accessibilityOpsPlanetTmp, accessibilityEpochPlanetTmp,
                                       dayOperationalBestTime[i_pl_true, i_flt, indxSNR, 0], 
                                       dayOperationalBestTime[i_pl_true, i_flt, indxSNR, 2] -
                                       dayOperationalBestTime[i_pl_true, i_flt, indxSNR, 0], 
                                       dayEpochBestTime[i_pl_true, i_flt, indxSNR, 2] -
                                       dayEpochBestTime[i_pl_true, i_flt, indxSNR, 0], 
                                       waMasBestTime[i_pl_true, i_flt, indxSNR, 0],
                                       waMasBestTime[i_pl_true, i_flt, indxSNR, 2],
                                       fRatioBestTime[i_pl_true, i_flt, indxSNR, 0],
                                       fRatioBestTime[i_pl_true, i_flt, indxSNR, 2])
                                    plt.text(0.1, pos[i_pl] - step + i_flt * width_bar - width_bar / 5, textString, fontdict = fontText)
                                else:
                                    textString = 'Access Ops:%s, Access Obs:%s' % (accessibilityOpsPlanetTmp, accessibilityEpochPlanetTmp)
                                    plt.text(0.1, pos[i_pl] - step + i_flt * width_bar - width_bar / 5, textString, fontdict = fontText)
                                    
                            
                                
            plt.axvline(x=0, color='k')
            # From https://riptutorial.com/matplotlib/example/14063/plot-with-gridlines
            plt.grid(axis='x', color='#666666', linestyle='-')
            plt.minorticks_on()
            plt.grid(which='minor', color='#999999', linestyle='-', alpha=0.2)
            ax.set_yticks(pos)
            ax.set_yticklabels(PNamePlot, size=fontSize)
            ax.set_ylim((-width_space, total_space+width_space))
            ax.set_xlabel('$\log_{10}$(Shortest Integration Time in Hours)', size=fontSize, labelpad=10)
            # Legend tips from https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width, box.height * 0.8])
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), fancybox=True, shadow=True, \
                      fontsize=fontSize, ncol=int(np.ceil(nFilters/3)))
            # Lots of warnings from ERFA due to uncertain leap seconds ... Maybe there's away to do it better, or turn off these warnings
            ciDateEpoch0 = Time(CGI_epoch0, format='byear').to_value('iso', subfmt='date')
            ciDateEpoch1 = Time(CGI_epoch1, format='byear').to_value('iso', subfmt='date')
            plt.title('CGI. %s/%s. Keep out angles for solar panels=[%1.1f,%1.f] deg' \
                      % (ciDateEpoch0, ciDateEpoch1, specs['koAngles_SolarPanel'][0], specs['koAngles_SolarPanel'][1]), size=fontSize)
                # Notice the use of 'tight' to let the y label ticks be inside the figure
            plt.savefig(dir_figures + 'rv_ci_perf_exosims_' + str(i_plt) + '.png', bbox_inches='tight')
            plt.tight_layout()
            ax.set_xlim(right=np.log10(maxIntTimeHours))
            ax.set_xlabel('$\log_{10}$(Shortest Integration Time in Hours). '\
                          'Axis cut at %1.1f hours (%1.1f days)' % (maxIntTimeHours, maxIntTimeHours / 24), size=fontSize, labelpad=10)
            plt.savefig(dir_figures + 'rv_ci_perf_exosims_' + str(i_plt) + '_' + str(maxIntTimeHours) + '.png', bbox_inches='tight')
            plt.tight_layout()
            plt.show()
            if indPlanet2 == nPlanetOK:
                break

#breakpoint
