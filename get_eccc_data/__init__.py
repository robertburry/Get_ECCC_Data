import pandas as pd
import numpy as np
name = 'get_eccc_data'


__doc__ = """ 
get_eccc_data - A Python package for retrieving historical ECCC data. 
======================================================================

**get_eccc_data** is a Python package that streamlines the retrieval of 
data from ECCC. A lot of the data from ECCC is open source, though can 
be difficult to retrieve. This is what is trying to be solved with this package. 
This package includes several functions representing the kind of data that is 
available. 

Functions
---------
import_station_list(): - Retrieve a list of stations available from ECCC. 
airport_search(): - Retrieve station information for an Airport.
import_climate_data(): - Retrieve climate data. 

Planned Additions
-----------------
import_metar(): - Retrieve metar data. ** Not Active Yet ** 
import_sounding(): - Retrieve atmospheric sounding data. ** Not Active Yet **
import_taf(): - Retrieve TAF's for an Airport. ** Not Active Yet ** 
"""


def import_station_list(downcast=True):
    """ Retrieves the list of available stations for ECCC Climate data. 
    This data is stored in a CSV file located on a public Google Drive.

    Arguments: 
        downcast (bool) - converts dataframe to types that fit default values better, default True

    Returns: 
        DataFrame
    """

    url = 'https://drive.google.com/file/d/1HDRnj41YBWpMioLPwAFiLlK4SK8NV72C/view'
    url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
    station_id = pd.read_csv(url, skiprows=3)
    station_id.drop(['Latitude', 'Longitude'], axis=1, inplace=True)

    if downcast:
        dcast_ids = ['Station ID', 'WMO ID']
        dcast_geo = ['Latitude (Decimal Degrees)',
                     'Longitude (Decimal Degrees)', 'Elevation (m)']

        dcast_yrs = [col for col in station_id.columns if 'Year' in col]

        station_id.loc[:, dcast_ids] = station_id.loc[:,
                                                      dcast_ids].astype(pd.Int32Dtype())
        station_id.loc[:, dcast_geo] = station_id.loc[:,
                                                      dcast_geo].astype(np.float16)
        station_id.loc[:, dcast_yrs] = station_id.loc[:,
                                                      dcast_yrs].astype(pd.Int16Dtype())

    return station_id


def airport_search(airport, station_id):
    """ Filters trough a dataframe to find the relevant information
    for climate data on a specific airport. 

    Arguments: 
        airport (str) - 3 Digit code for Canadian Airports.
        station_id (pd.DataFrame) - a list of station ID's with airport codes.

    Possible use: 
        Filter through a DataFrame to get only the information relevant to
        a specific airport. Limits within Canada.

    Returns:
        DataFrame 
    """

    if not isinstance(station_id, pd.DataFrame):
        raise TypeError('station_id input must be a Pandas DataFrame.')

    if not isinstance(airport, str):
        raise TypeError('Airport needs to be a string')

    if 'TC ID' not in station_id.columns:
        raise ValueError(
            'dataframe nees a column with TC ID like is found in original document')

    if len(airport) > 3 or len(airport) <= 2:
        raise ValueError('Airport code needs to be 3 characters')

    airport_filtered = station_id[station_id['TC ID'] == airport]

    return airport_filtered


def import_climate_data(yr, stn, prov, freq='monthly', mths=None):
    """ Imports Climate Data directly from the website source given in the MSC usersguide. 
    There is a wget command that could be used as well which could make this faster. However, 
    due to wget not being updated in a few years it was decided to go this route. 

    Arguments: 
        freq (str) - Frequency that  user wants data for, default monthly.
        yr (List[int]) - Years the user wants data for.
        stn (int) - Station ID the users want data for.
        prov (str) - Province that stn is located.

    Returns:
        DataFrame 
    """

    if not isinstance(yr, list):
        raise TypeError('Year must be list or range.')

    if not isinstance(freq, str):
        raise ValueError('Frequency must be a string.')

    if not isinstance(stn, (int, str)):
        raise ValueError('Station ID must be an integer.')

    if not isinstance(prov, str):
        raise ValueError('Province must be a string.')

    if (freq.lower() != 'monthly') and (freq.lower() != 'daily'):
        raise ValueError('Frequency must be either Monthly or Daily.')

    if (freq.lower() != 'monthly') and mths is None:
        raise TypeError('Months must be a list or a range')

    if freq.lower() == 'monthly':
        urls = []
        freq = freq.lower()
        ec_code = 'P1M'
        for x in yr:
            dump = f"https://dd.weather.gc.ca/climate/observations/{freq}/csv/{prov}/climate_{freq}_{prov}_{stn}_{x}_{ec_code}.csv"
            urls += [dump]

        # Builds DF from all the URLS
        df = pd.concat(pd.read_csv(x, encoding='unicode_escape') for x in urls)

        df.drop(['D', 'S%N', 'P%N', 'BS', 'BS%'], axis=1, inplace=True)

        wanted_names = {'Tm': 'Mean Temperature (°C)',
                        'DwTm': 'Days with Valid Mean Temperature',
                        'Tx': 'Highest Monthly Maximum Temperature (°C)',
                        'DwTx': 'Days with Valid Maximum Temperature',
                        'Tn': 'Lowest Monthly Minimum Temperature (°C)',
                        'DwTn': 'Days with Valid Minimum Temperature',
                        'S': 'Total Snowfall (cm)',
                        'DwS': 'Days with Valid Snowfall',
                        'P': 'Total Precipitation (mm)',
                        'DwP': 'Days with Valid Precipitation',
                        'S_G': 'Snow on the ground last day (cm)',
                        'Pd': 'Number of days with Precipitation 1.0 mm or more',
                        'DwBS': 'Days with Valid Bright Sunshine',
                        'HDD': 'Heating Degree Days',
                        'CDD': 'Cooling Degree Days'}

        df.rename(columns=wanted_names, inplace=True)
        return df
    else:
        urls = []
        freq = freq.lower()
        ec_code = 'P1D'
        for x in yr:
            for y in mths:
                dump = f"https://dd.weather.gc.ca/climate/observations/{freq}/csv/{prov}/climate_{freq}_{prov}_{stn}_{x}-{y:02d}_{ec_code}.csv"
                urls += [dump]

        df = pd.concat(pd.read_csv(x, encoding='unicode_escape') for x in urls)
        return df
