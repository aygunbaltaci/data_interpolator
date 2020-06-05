# Data Interpolator

These scripts interpolate two datasets with different resolutions to one another. 

**interpolator_highresolution.py**: It interpolates the low resolution data to the high resolution data based on the input in the 1st column of the provided input files (e.g. Time data).
**interpolator_lowresolution.py**: It interpolates the high resolution data to the low resolution data based on the input in the 1st column of the provided input files.

## Why Useful? 
Let's say that you collect some measurement data, one from a GPS module and one from the flight controller of UAV. Each log file has different time resolution (e.g. GPS module records data every 0.1 s and flight controller every 1 s), then you can use this program to interpolate the data from GPS module (data with high resolution) to the data from flight 
controller (data with low resolution). This way, you can combine both data files for data analytics, graph generation, etc. 

## Prerequisites
**Python 3**
> sudo apt update

> sudo apt install python3.6 (or any other python3 version) 

**Csv and numpy libraries**
> pip3 install csv numpy

## Input Files
**inputfiles/data_highresolution.csv**: High resolution dataset
**inputfiles/data_lowresolution.csv**: Low resolution dataset

## Usage
> python3 interpolator_highresolution.py

> python3 interpolator_lowresolution.py

## Result
The result is saved in the directory below with the corresponding date (YYYYMMDD_HHMMSS):
*outputfiles/*

Perform *Text to Columns* conversion with *space* character as delimeter on the output csv file. 

## Copyright
This code is licensed under GNU General Public License v3.0. For further information, please refer to [LICENSE](LICENSE)