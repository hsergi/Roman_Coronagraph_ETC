#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Generic packages
import hjson, json, os
import numpy as np
from pathlib import Path
# For integration times
import astropy.units as u
# For keep outs and to convert decimal dates into readable dates
import EXOSIMS
from astropy.time import Time
from scripts.cgi_etc_star_accessibility import cgi_etc_star_accessibility
# Updated specs for EXOSIMS
from scripts.cgi_etc_update_specs import cgi_etc_update_specs
# CSV file
from scripts.store_csv_file import store_csv_file_sl

def cgi_etc_sl(CGI_epoch0, CGI_epoch1, filterList, jsonFile, 
    csvFileName, CGI_Observations): 
    """
     Script that derives the shortest integration times to achieve SNR=5 or 10.
     For SL planets, we do not extract ephemeris data from IMD, 
     but from the literature, until it is up to date.
    """ 

    # Self-Luminous planets.
    PName = CGI_Observations['PName']
        
    # Planet name with the star's name from HIP catalogue. P.S. write a function to translate HIP numbers into common names
    hipPName = CGI_Observations['hipPName']
    nPlanets = len(hipPName)
    nPlanetsCommon = len(PName)
    if (nPlanets != nPlanetsCommon):
    	raise ValueError("The number of HIP and common names is different. Please fix it")

    # Derive the star's accessibility
    # 10/28/21: coming soon
    cgi_etc_star_accessibility(CGI_epoch0, CGI_epoch1, jsonFile,
        csvFileName, PName, hipPName)
    
    # Write star names
    starName = [''] * nPlanets
    starNameCommon = [''] * nPlanets
    for i_pl in np.arange(nPlanets):
        starName[i_pl] = hipPName[i_pl][0:len(hipPName[i_pl])-2] 
        starNameCommon[i_pl] = PName[i_pl][0:len(PName[i_pl])-2]
       
    WA = CGI_Observations['WA_arcsec'] * u.arcsec
    d = CGI_Observations['d_AU'] * u.AU
    I = CGI_Observations['I_deg'] * u.deg
    # Point source flux ratios:
    try:
        FR_NF_Imager = np.array(CGI_Observations['FR_NF_Imager'])
    except:
        FR_NF_Imager = np.empty((nPlanets))
        FR_NF_Imager.fill(np.nan)
    try:
        FR_Amici_Spec = np.array(CGI_Observations['FR_Amici_Spec'])
    except:
        FR_Amici_Spec = np.empty((nPlanets))
        FR_Amici_Spec.fill(np.nan)
    try:
        FR_WF_Imager = np.array(CGI_Observations['FR_WF_Imager'])
    except:
        FR_WF_Imager = np.empty((nPlanets))
        FR_WF_Imager.fill(np.nan)
     
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
    
    # SNR list
    SNRList = CGI_Observations['SNRList']
    nSNR = len(SNRList)
    # Storing the integration times
    intTimeFilterHours = np.empty([nFilters,nPlanets,nSNR], dtype=float)
    intTimeFilterHours.fill(np.nan)
    PNameFilter = [[''] * nFilters for ll in range(nPlanets)]
    # Loop over filters
    for i_flt in np.arange(nFilters):
        # Updating the instrumental specs because of the different post-processing factor for each filter
        kppTmp, OSTmp, TLTmp, TKTmp = \
            cgi_etc_update_specs(jsonFile, filterList[i_flt], 
            CGI_epoch0, CGI_epoch1)
        kppList[i_flt] = kppTmp
        mode = list(filter(lambda mode: mode['instName'] == filterList[i_flt], OSTmp.observingModes))[0]
        print( mode['instName'])
        # Indices where the planet is in the original list
        pIndsOK = np.empty(0, dtype=int)
        # Indices where the star is
        sIndsOK = np.empty(0, dtype=int)
        # Sentinel
        i_pl_OK = 0
        for i_pl in np.arange(nPlanets):
            tmp = np.where(TLTmp.Name == starName[i_pl])
            if np.size(tmp) != 0:
                pIndsOK = np.append(pIndsOK, i_pl_OK)
                sIndsOK = np.append(sIndsOK, tmp[0][0])
                i_pl_OK += 1
            else:
                print('WARNING: planet %s is not in the catalog.' % (starName[i_pl]))
            
        # Update the list of planets with those available, as well as their host stars and properties
        nPlanetsOK = np.size(pIndsOK)
        starNameOK = [''] * nPlanetsOK
        WAOK = [u.arcsec] * nPlanetsOK
        dOK = [u.AU] * nPlanetsOK
        IOK = [u.deg] * nPlanetsOK
        FR_NF_ImagerOK = np.empty(nPlanetsOK, dtype=float)
        FR_NF_ImagerOK.fill(np.nan)
        FR_Amici_SpecOK = np.empty(nPlanetsOK, dtype=float)
        FR_Amici_SpecOK.fill(np.nan)
        FR_WF_ImagerOK = np.empty(nPlanetsOK, dtype=float)
        FR_WF_ImagerOK.fill(np.nan)
        for i_pl in np.arange(nPlanetsOK):
            PNameFilter[i_pl][i_flt] = PName[pIndsOK[i_pl]]
            WAOK[i_pl] = WA[pIndsOK[i_pl]]
            dOK[i_pl] = d[pIndsOK[i_pl]]
            IOK[i_pl] = I[pIndsOK[i_pl]]
            FR_NF_ImagerOK[i_pl] = FR_NF_Imager[pIndsOK[i_pl]]
            FR_Amici_SpecOK[i_pl] = FR_Amici_Spec[pIndsOK[i_pl]]
            FR_WF_ImagerOK[i_pl] = FR_WF_Imager[pIndsOK[i_pl]]
        
        # Write star names
        for i_pl in np.arange(nPlanetsOK):
            starNameOK[i_pl] = TLTmp.Name[sIndsOK]
    
        # Local zodi
        fZ = TLTmp.ZodiacalLight.fZ0
        if (mode['instName'] == 'CONS_NF_Imager') or (mode['instName'] == 'OPTI_NF_Imager'):
            dMag =  -2.5 * np.log10(FR_NF_ImagerOK)
        if (mode['instName'] == 'CONS_Amici_Spec') or (mode['instName'] == 'OPTI_Amici_Spec'):
            dMag =  -2.5 * np.log10(FR_Amici_SpecOK)
        if (mode['instName'] == 'CONS_WF_Imager') or (mode['instName'] == 'OPTI_WF_Imager'):
            dMag = -2.5 * np.log10(FR_WF_ImagerOK)
    
        for i_snr in np.arange(nSNR):
            mode['SNR'] = SNRList[i_snr] 
            # Loop over planets
            for i_pl in range(nPlanetsOK):
                # Notice the twisted way to pass the object for the method to work
                ITmp = [IOK[i_pl].to('deg').value] * u.deg
                fEZ = TLTmp.ZodiacalLight.fEZ(np.array([TLTmp.MV[sIndsOK[i_pl]]]), ITmp, dOK[i_pl])
                tmp = OSTmp.calc_intTime(TLTmp, np.array([sIndsOK[i_pl]]), fZ, fEZ, \
                                      dMag[i_pl], WAOK[i_pl], mode, TK=TKTmp).to('hour').value[0]
                if np.isnan(tmp) == False and tmp != 0:
                    intTimeFilterHours[i_flt, i_pl, i_snr] = tmp

    ####################################
    # (Optional) Print out the results #
    ####################################
    
   # change 0 by 1 to print the results on screen
    if 0: 
        for i_snr in np.arange(nSNR):
            print('\nInt time (hours, SNR=%1.1f)\n' % (SNRList[i_snr]))
            fText = ''      
            for i_flt in np.arange(nFilters):    
                fText = fText + '%s (kpp=%1.2f) \t' % (filterList[i_flt], kppList[i_flt])
            print(fText)
            # Beware that PNameFilter is a multi-dimensional list
            for i_pl in np.arange(len(PNameFilter)):
                pText = ''
                control=''
                for i_flt in np.arange(len(PNameFilter[0])):
                    if PNameFilter[i_pl][i_flt] != '':
                        pText = pText + '%s: %1.2f \t' % (PNameFilter[i_pl][i_flt], \
                                                          intTimeFilterHours[i_flt, i_pl, i_snr])
                    else:
                        pText = pText + 'Unavailable \t'
                        control = control + 'Unavailable \t'
                if pText != control:
                    print(pText)

    ###################################
    # Store the results in a CVS file #
    ###################################
    store_csv_file_sl(filterList, kppList, PNameFilter, WAOK, dOK, 
        IOK, FR_NF_ImagerOK, FR_Amici_SpecOK, FR_WF_ImagerOK, 
        SNRList, intTimeFilterHours, csvFileName)

