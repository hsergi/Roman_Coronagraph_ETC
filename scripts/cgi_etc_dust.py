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
# Updated specs for EXOSIMS
from scripts.cgi_etc_update_specs import cgi_etc_update_specs
# CSV file
from scripts.store_csv_file import store_csv_file_ed

def cgi_etc_dust(CGI_epoch0, CGI_epoch1, filterList, jsonFile, csvFileName, CGI_Observations):
    
    # Systems to consider
    starNameCommon = CGI_Observations['starNameCommon']

    # Corresponding HIP id
    starNameHip = CGI_Observations['starNameHip']
    nCases = len(starNameHip)
    nCasesCommon = len(starNameCommon)
    if (nCases != nCasesCommon):
    	raise ValueError("The number of HIP and common names is different. Please fix it")

    # Derive the star's accessibility
    # Adding a dummy label to use the same method as for all targets
    starNameCommonZ = [''] * nCases
    starNameHipZ = [''] * nCases
    for idx in range(len(starNameHip)):
        starNameCommonZ[idx] = starNameCommon[idx] + ' z'
        starNameHipZ[idx] = starNameHip[idx] + ' z'
    # 10/28/21: coming soon
    #cgi_etc_star_accessibility(CGI_epoch0, CGI_epoch1, jsonFile,
    #    csvFileName, starNameCommonZ, starNameHipZ)

    WA = CGI_Observations['WA_arcsec'] * u.arcsec
    # Equivalent point-like flux ratios:
    try:
        FR_NF_Imager = np.array(CGI_Observations['FR_NF_Imager'])
    except:
        FR_NF_Imager = np.empty((nCases))
        FR_NF_Imager.fill(np.nan)
    try:
        FR_Amici_Spec = np.array(CGI_Observations['FR_Amici_Spec'])
    except:
        FR_Amici_Spec = np.empty((nCases))
        FR_Amici_Spec.fill(np.nan)
    try:
        FR_WF_Imager = np.array(CGI_Observations['FR_WF_Imager'])
    except:
        FR_WF_Imager = np.empty((nCases))
        FR_WF_Imager.fill(np.nan)

    ## P.S. d and I are irrelevant since exozodi will be zeroed later on
    ## Actual planet-star distance and visual inclination (used for exozodi)
    d = [10] * len(CGI_Observations['WA_arcsec']) * u.AU
    ## Notice that for large distances planet-star, the exozodi becomes negligible
    I = [20] * len(CGI_Observations['WA_arcsec']) * u.deg

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
    intTimeFilterHours = np.empty([nFilters,nCases,nSNR], dtype=float)
    intTimeFilterHours.fill(np.nan)
    pNameFilter = [[''] * nFilters for ll in range(nCases)]
    # Loop over filters
    for i_flt in np.arange(nFilters):
        # Updating the instrumental specs because of the different post-processing factor for each filter.
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
        for i_pl_OK in np.arange(nCases):
            tmp = np.where(TLTmp.Name == starNameHip[i_pl_OK])
            if np.size(tmp) != 0:
                pIndsOK = np.append(pIndsOK , i_pl_OK)
                sIndsOK = np.append(sIndsOK, tmp[0][0])
                i_pl_OK += 1
            else:
                print('WARNING: star %s is not in the catalog.' % (starNameHip[i_pl_OK]))

        for i_pl in np.arange(nCases):
            pNameFilter[i_pl][i_flt] = starNameCommon[pIndsOK[i_pl]]

        # Local zodi
        fZ = TLTmp.ZodiacalLight.fZ0
        if (mode['instName'] == 'CONS_NF_Imager') or (mode['instName'] == 'OPTI_NF_Imager'):
            dMag =  -2.5 * np.log10(FR_NF_Imager)
        if (mode['instName'] == 'CONS_Amici_Spec') or (mode['instName'] == 'OPTI_Amici_Spec'):
            dMag =  -2.5 * np.log10(FR_Amici_Spec)
        if (mode['instName'] == 'CONS_WF_Imager') or (mode['instName'] == 'OPTI_WF_Imager'):
            dMag = -2.5 * np.log10(FR_WF_Imager)

        for i_snr in np.arange(nSNR):
            mode['SNR'] = SNRList[i_snr]
            # Loop over planets
            for i_pl in range(nCases):
                # Notice the twisted way to pass the object for the method to work
                ITmp = [I[i_pl].to('deg').value] * u.deg
                ##Notice how the entry for exozodi is set to zero. In the case of exozodiacal light and debris disks, we do not want to add any additional dust to the point-like equivalent flux ratio.
                tmp = OSTmp.calc_intTime(TLTmp, np.array([sIndsOK[i_pl]]), fZ, 0*fZ, \
                                      dMag[i_pl], WA[i_pl], mode, TK=TKTmp).to('hour').value[0]
                if np.isnan(tmp) == False and tmp != 0:
                    intTimeFilterHours[i_flt, i_pl, i_snr] = tmp

    ###################################
    # Store the results in a CVS file #
    ###################################
    store_csv_file_ed(filterList, kppList, pNameFilter, WA,
        FR_NF_Imager, FR_Amici_Spec, FR_WF_Imager, SNRList,
        intTimeFilterHours, csvFileName)

    ####################################
    # (Optional) Print out the results #
    ####################################

    if 0:
        for i_snr in np.arange(nSNR):
            print('\nInt time (hours, SNR=%1.1f)\n' % (SNRList[i_snr]))
            fText = ''
            for i_flt in np.arange(nFilters):
                fText = fText + '%s (kpp=%1.2f) \t' % (filterList[i_flt], kppList[i_flt])
            print(fText)
            # Beware that pNameFilter is a multi-dimensional list
            for i_pl in np.arange(len(pNameFilter)):
                pText = ''
                control=''
                for i_flt in np.arange(len(pNameFilter[0])):
                    if pNameFilter[i_pl][i_flt] != '':
                        pText = pText + '%s: %1.3f \t' % (pNameFilter[i_pl][i_flt], \
                                                          intTimeFilterHours[i_flt, i_pl, i_snr])
                    else:
                        pText = pText + 'Unavailable \t'
                        control = control + 'Unavailable \t'
                if pText != control:
                    print(pText)
