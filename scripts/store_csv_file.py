#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Global constant
from config import INSTALLATION_PATH
# Generic packages
import os
import numpy as np
import pandas as pd

def store_csv_file_acc(starNameCommon, koGood, len_koEvaltimes, \
    CGI_epoch0, csvFileName):
    """
    PURPOSE
    -------

        Store the accessibility of the targets
    """

    # Create a data frame:
    # Star name       target 1 (average, %)   target 1  ...

    # Create the folder where the figures will be stored
    dir_csv = INSTALLATION_PATH 
    if dir_csv[-1] != '/':
        dir_csv += '/output/csv/'
    else:
        dir_csv += 'output/csv/'
    if os.path.exists(dir_csv) == False:
        os.mkdir(dir_csv)
    
    dictCI = {}
    if len(starNameCommon) == 1:
        dictCI[f'{starNameCommon[0]:s} (average, %)'] = \
        np.round(np.sum(koGood) / len_koEvaltimes * 100, 2)
        dictCI[f'{starNameCommon[0]:s} (days after {CGI_epoch0:.4f})'] = \
            koGood
    else:
        for star in range(len(starNameCommon)):
            dictCI[f'{starNameCommon[star]:s} (average, %)'] = \
            np.round(np.sum(koGood[star]) / len_koEvaltimes * 100, 2)
            dictCI[f'{starNameCommon[star]:s} (days after {CGI_epoch0:.4f})'] = \
            koGood[star]

    df = pd.DataFrame.from_dict(dictCI)
    for star in range(len(starNameCommon)):
        df[f'{starNameCommon[star]:s} (average, %)'][1:] = np.nan

    if csvFileName.find('.') < 1:
        csvFileName += '.csv'
    csvFileName = 'accessibility_' + csvFileName
    df.to_csv(dir_csv+csvFileName, header=True, encoding='utf-8')

def store_csv_file_sl(filterList, kppList, PNameFilter, WA, d, I,
        FR_NF_Imager, FR_Amici_Spec, FR_WF_Imager, SNRList,
        intTimeFilterHours, csvFileName):
    """
    PURPOSE
    -------

        Script that stores the estimated integration times of self-luminous
            exoplanets as a CSV file
    """

    # Create the 2-dimensional data frame:
    #  Planet name           Planet 1     Planet 2 ...
    #  WA (mas)
    #  d (AU)
    #  I (deg)
    #  Filter (kpp=...)
    #  Flux ratio
    #  TimeToSNR# ... (hours)
    #  ...
    #  TimeToSNR# ... (hours)
    #  Filter (kpp=...)
    #  ...

    # Create the folder where the figures will be stored
    dir_csv = INSTALLATION_PATH
    if dir_csv[-1] != '/':
        dir_csv += '/output/csv/'
    else:
        dir_csv += 'output/csv/'
    if os.path.exists(dir_csv) == False:
        os.mkdir(dir_csv)

    dictCI = {'Planet name': [],
        'WA (mas)': [], 
        'd (AU)': [],
        'I (deg)': []}
    for planet in range(len(PNameFilter)):
        dictCI['Planet name'].append(PNameFilter[planet][0])
        dictCI['WA (mas)'].append(WA[planet].value * 1000)
        dictCI['d (AU)'].append(d[planet].value)
        dictCI['I (deg)'].append(I[planet].value)
    for filter in range(len(filterList)):
        if (filterList[filter] == 'CONS_NF_Imager' \
                or filterList[filter] == 'OPTI_NF_Imager') \
                and not np.isnan(np.sum(FR_NF_Imager)):
            dictCI['Flux ratio (NF)'] = FR_NF_Imager
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PNameFilter)
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PNameFilter)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeFilterHours[filter][planet][snr],
                        decimals=3))
        if (filterList[filter] == 'CONS_Amici_Spec' \
                or filterList[filter] == 'OPTI_Amici_Spec') \
                and not np.isnan(np.sum(FR_Amici_Spec)):
            dictCI['Flux ratio (Spec)'] = FR_Amici_Spec
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PNameFilter)
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PNameFilter)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeFilterHours[filter][planet][snr],
                        decimals=3))
        if (filterList[filter] == 'CONS_WF_Imager' \
                or filterList[filter] == 'OPTI_WF_Imager') \
                and not np.isnan(np.sum(FR_WF_Imager)):
            dictCI['Flux ratio (WF)'] = FR_WF_Imager
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PNameFilter)
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PNameFilter)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeFilterHours[filter][planet][snr],
                        decimals=3))

    df = pd.DataFrame.from_dict(dictCI)
    df = df.T
    if csvFileName.find('.') < 1:
        csvFileName += '.csv'
    df.to_csv(dir_csv+csvFileName, header=False, encoding='utf-8')

def store_csv_file_rv(filterList, kppList, PName,
        dayEpochBestTime, waMasBestTime, fRatioBestTime,
        SNRList, intTimeBestHours,
        csvFileName):
    """
    PURPOSE:
    Script that stores the estimated integration times of reflected light
    exoplanets as a CSV file
    """

    # Create the 2-dimensional data frame:
    #  Planet name           Planet 1     Planet 2 ...
    #  Filter (kpp=...)
    #  Day of Mission
    #  WA (mas)
    #  Flux ratio
    #  TimeToSNR# ... (hours)
    #  ...
    #  TimeToSNR# ... (hours)
    #  Filter (kpp=...)
    #  Day of Mission
    #  WA (mas)
    #  ...

    # Create the folder where the figures will be stored
    dir_csv = INSTALLATION_PATH
    if dir_csv[-1] != '/':
        dir_csv += '/output/csv/'
    else:
        dir_csv += 'output/csv/'
    if os.path.exists(dir_csv) == False:
        os.mkdir(dir_csv)

    dictCI = {'Planet name': []}
    for planet in range(len(PName)):
        dictCI['Planet name'].append(PName[planet])
    for filter in range(len(filterList)):
        if (filterList[filter] == 'CONS_NF_Imager' \
                or filterList[filter] == 'OPTI_NF_Imager'):
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PName)
            dictCI[f'DoM_{filterList[filter]:s}'] = \
                np.round(dayEpochBestTime[:, filter, 0, 1], decimals=1)
            dictCI[f'WA_{filterList[filter]:s} (mas)'] = \
                np.round(waMasBestTime[:,filter, 0, 1], decimals=1)
            dictCI[f'FR_{filterList[filter]:s}'] = \
                fRatioBestTime[:,filter, 0, 1]
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PName)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeBestHours[planet][filter][snr],
                        decimals=3))

    for filter in range(len(filterList)):
        if (filterList[filter] == 'CONS_Amici_Spec' \
                or filterList[filter] == 'OPTI_Amici_Spec'):
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PName)
            dictCI[f'DoM_{filterList[filter]:s}'] = \
                np.round(dayEpochBestTime[:, filter, 0, 1], decimals=1)
            dictCI[f'WA_{filterList[filter]:s} (mas)'] = \
                np.round(waMasBestTime[:,filter, 0, 1], decimals=1)
            dictCI[f'FR_{filterList[filter]:s}'] = \
                fRatioBestTime[:,filter, 0, 1]
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PName)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeBestHours[planet][filter][snr],
                        decimals=3))

    for filter in range(len(filterList)):
        if (filterList[filter] == 'EB_WF_Imager' \
                or filterList[filter] == 'DRM_WF_Imager'):
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PName)
            dictCI[f'DoM_{filterList[filter]:s}'] = \
                np.round(dayEpochBestTime[:, filter, 0, 1], decimals=1)
            dictCI[f'WA_{filterList[filter]:s} (mas)'] = \
                np.round(waMasBestTime[:,filter, 0, 1], decimals=1)
            dictCI[f'FR_{filterList[filter]:s}'] = \
                fRatioBestTime[:,filter, 0, 1]
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PName)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeBestHours[planet][filter][snr],
                        decimals=3))

    df = pd.DataFrame.from_dict(dictCI)
    df = df.T
    if csvFileName.find('.') < 1:
        csvFileName += '.csv'
    df.to_csv(dir_csv+csvFileName, header=False, encoding='utf-8')

def store_csv_file_ed(filterList, kppList, PNameFilter, WA,
        FR_NF_Imager, FR_Amici_Spec, FR_WF_Imager, SNRList,
        intTimeFilterHours, csvFileName):
    """
    PURPOSE:
    Script that stores the estimated integration times of exo-dust
    targets as a CSV file
    """

    # Create the 2-dimensional data frame:
    #  Planet name           Planet 1     Planet 2 ...
    #  WA (mas)
    #  Filter (kpp=...)
    #  Flux ratio
    #  TimeToSNR# ... (hours)
    #  ...
    #  TimeToSNR# ... (hours)
    #  Filter (kpp=...)
    #  ...

    # Create the folder where the figures will be stored
    dir_csv = INSTALLATION_PATH
    if dir_csv[-1] != '/':
        dir_csv += '/output/csv/'
    else:
        dir_csv += 'output/csv/'
    if os.path.exists(dir_csv) == False:
        os.mkdir(dir_csv)

    dictCI = {'Disk name': [],
        'WA (mas)': []}
    for planet in range(len(PNameFilter)):
        dictCI['Disk name'].append(PNameFilter[planet][0])
        dictCI['WA (mas)'].append(WA[planet].value * 1000)
    for filter in range(len(filterList)):
        if (filterList[filter] == 'CONS_NF_Imager' \
                or filterList[filter] == 'OPTI_NF_Imager') \
                and not np.isnan(np.sum(FR_NF_Imager)):
            dictCI['Flux ratio (NF)'] = FR_NF_Imager
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PNameFilter)
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PNameFilter)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeFilterHours[filter][planet][snr],
                        decimals=3))
        if (filterList[filter] == 'CONS_Amici_Spec' \
                or filterList[filter] == 'OPTI_Amici_Spec') \
                and not np.isnan(np.sum(FR_Amici_Spec)):
            dictCI['Flux ratio (Spec)'] = FR_Amici_Spec
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PNameFilter)
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PNameFilter)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeFilterHours[filter][planet][snr],
                        decimals=3))
        if (filterList[filter] == 'CONS_WF_Imager' \
                or filterList[filter] == 'OPTI_WF_Imager') \
                and not np.isnan(np.sum(FR_WF_Imager)):
            dictCI['Flux ratio (WF)'] = FR_WF_Imager
            dictCI[filterList[filter]+f' (kpp={kppList[filter]:0.2f})'] = \
            [''] * len(PNameFilter)
            for snr in range(len(SNRList)):
                SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'] = []
                for planet in range(len(PNameFilter)):
                    SNR_str=f'{SNRList[snr]:.1f}'.replace(".","p")
                    dictCI[f'T_{filterList[filter]:s}_SNR{SNR_str:s} ' +
                        f'(hours)'].append(
                        np.round(intTimeFilterHours[filter][planet][snr],
                        decimals=3))

    df = pd.DataFrame.from_dict(dictCI)
    df = df.T
    if csvFileName.find('.') < 1:
        csvFileName += '.csv'
    df.to_csv(dir_csv+csvFileName, header=False, encoding='utf-8')
