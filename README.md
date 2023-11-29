# Get_ECCC_Data

![Tests](https://github.com/robertburry/Get_ECCC_Data/actions/workflows/tests.yml/badge.svg)

This is to easily retrieve open-source data provided from ECCC. 

## Motivation 
The motivation of this project is to create an all encompassing resource for users to find the 
data produced by Environment and Climate Change Canada (ECCC). ECCC is the governing Meteorological Agency
within Canada, and as a member of the World Meteorological Organization (WMO) there is an encouagement to 
have the majority of the data/products produced be open-source. 

As such ECCC has been doing this more and more often. However, the problem is that a lot of the raw data people want (whether that be for analysis, curiosity, etc.) can be very difficult to locate where it is hosted. But also with some data it can be found in multiple locations, or reference different locations. 

So the goal of this is to provide a user with a much easier experience to get this kind of data. 

As part of ECCC's open data policy they have created their own Data Use License, which every uses of this project is enoucaged to read this so they know the expectations of the data itself. The use of this project is, and will always remain, open-source. 

## Disclaimer
This is currently not made in collaboration with ECCC, and as such this project does not reflect the intentions or opinions of ECCC.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install get_eccc_data.

```bash
pip install get-eccc-data
```

If you are looking to use this on a cloud computer like Google Collab or another jupyter notebook you will have to insert a % or ! depending on what you are using. 

Google Collab Example:

``` bash
!pip install get-eccc-data
```

## Overview of get_eccc_data

get_eccc_data is a Python library for extracting with ECCC data sourced from their "DataMart". There are two main datamarts one is a [barebones site](https://dd.weather.gc.ca), this only houses text-ony data, then another [more modern GitHub](https://eccc-msc.github.io/open-data/msc-data/readme_en/). The ladder houses some text products but mainly geared towards visual products, different file formats.

Currently includes import functions for a complete station list, a filter to sort a complete station list by an 3 code Airport identifier (i.e.: use YYZ for Toronto international, not CYYZ), and another function to import Monthly or Daily climate data (user choice) for a specific station ID. 

A future update will hopefully shorten the amount of fuctions, and make them more dynamic. However, I felt this was a good starting point to figure out what people would like to see added. 

## Usage

**Recommended importing**
```python
import get_eccc_data as ec
```

**Getting Station ID list**

```python
ec.import_station_list(downcast=True)
```

Returns a complete station information kept by ECCC. 

downcast
: optional, converts certain ID columns from float64 columns to int32, reduced Lat-Long Coordinates and elevation from float64 to float16, and converts years from float64 to int16. The goal of this is to reduce memory load if the user wants the full stations IDs dataframe. 

**Filtering by Airport**

```python
ec.airport_search(airport, station_id)
```

Returns a filtered dataframe depending on what airport the user desired. 

airport
: required, 3 letter station ID. Example (YYZ = Pearson International in Toronto)

station_id
: required, a dataframe that hosts station IDs. Note: In this current version station_id need to have the "TC ID" column found from the station list function. This will be improved, or combined in future builds. 

**Getting Climate Data** 

```python
ec.import_climate_data(yr, stn, prov, freq='monthly', mths=None)
```

Returns a dataframe for climate data for the specified location and timeframe.

yr
: required, a list or range of years you want data for. 

stn
: required, a string or integer of the station ID provided by ECCC. 

prov
: required, a string of the 2 Alpha code for a province/territory (i.e.: 'AB' for Alberta)

freq
: optional, a string for what frequency of data you would like. freq is set to 'monthly' by default. Currently the only two options available are 'Monthly' or 'Daily'.

mths
: optional, a range of numeric months you want to get daily data for. Set to 'None' by default. If changed you MUST change freq to 'Daily'. 


## Recognition
I would like to reconize that ECCC is making this data public, and open-source, allowing for projects like this to exist. I would also like to thank [mCoding](https://github.com/mCodingLLC/) for their videos helping people learn effective coding skills. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)