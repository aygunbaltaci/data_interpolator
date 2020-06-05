#!/usr/bin/env python3

#####################################################
# 04.06.2020
#
# This code takes two input files: 
# inputfiles/data_lowresolution.csv
# inputfiles/data_highresolution.csv
# 
# It interpolates the data with low resolution  
# to the data with high resolution based on the input  
# in the 1st column of the input files (e.g. Time data)
#
# ###### WHY USEFUL?
# 
# Let's say that you collect some measurement data,
# one from a GPS module and one from the flight
# controller of UAV. Each log file has different time
# resolution (e.g. GPS module records data every 0.1 s
# and flight controller every 1 s), then you can use 
# this program to interpolate the data from flight 
# controller (data with low resolution) to the data from
# GPS module (data with high resolution). This way, you
# can combine both data files for data analytics, graph
# generation, etc. 
# 
# Prerequisites: pip3 install csv numpy
#
# Author: Aygün Baltaci
#
# License: GNU General Public License v3.0
#####################################################

import csv
from datetime import datetime
import numpy as np
import os
import sys

# ============= Variables
fileDate = datetime.now().strftime('%Y%m%d_%H%M%S')
lowResInputFile = 'data_lowresolution.csv'
highResInputFile = 'data_highresolution.csv'
outputFile = '_datainterpolation_highresolution_output'
outputFileFormat = '.csv'
inputDir = 'inputfiles'
outputDir = 'outputfiles'
outputFileName = fileDate + outputFile + outputFileFormat
inputFileDelimeter = ','
outputFileDelimeter = ' '
defaultEncoding = 'utf-8-sig'
data_lowresolution = []
data_lowresolution_int = []
data_highresolution = []
concatRow = []
headerRow = []
headerRow2 = []

# ============= Nearest Point Interpolator
def lookupNearest(x0): # taken from https://stackoverflow.com/questions/31734471/2d-nearest-neighbor-interpolation-in-python
    xi = np.abs(data_lowresolution_int[0] - x0).argmin() # xi is the row number of the closest value in data_highresolution[0] to x0 
    return xi
    
# ============= Fetch low resolution data
with open(inputDir + os.sep + lowResInputFile, 'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = inputFileDelimeter)
    
    # Fetch the data_lowresolution from each row
    for row in plots:
        data_lowresolution.append(row)
        data_lowresolution_int.append(0)
    
    data_lowresolution = list(map(list, zip(*data_lowresolution))) # transpose the data_lowresolution: rows -> columns
    
    # Update default label names if labels are given in the input file
    if not (data_lowresolution[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same
        for i in range(len(data_lowresolution)): # Delete labels
            headerRow.append(data_lowresolution[i][0])
            del data_lowresolution[i][0]
    
    # Convert input data_lowresolution to float and to int
    for i in range(len(data_lowresolution)): # iterate over each column    
        data_lowresolution[i] = list(map(float, data_lowresolution[i]))  # convert data_lowresolution to float
        data_lowresolution_int[i] = list(map(int, data_lowresolution[i]))  # convert data_lowresolution to int

# ============= Fetch high resolution data
with open(inputDir + os.sep + highResInputFile,'r', encoding = defaultEncoding) as csvfile:
    plots = csv.reader(csvfile, delimiter = inputFileDelimeter)
    
    # Fetch the high resolution data from each row
    for row in plots:
        data_highresolution.append(row)
    
    data_highresolution = list(map(list, zip(*data_highresolution))) # transpose the data_lowresolution: rows -> columns
    
    # Update default label names if labels are given in the input file
    if not (data_highresolution[0][0].isdigit()): # only check one of the first-row entries. If one of them is not a number, then the other first-row entries should be the same        
        for i in range(len(data_highresolution)): # Delete labels
            headerRow2.append(data_highresolution[i][0])
            del data_highresolution[i][0]
        headerRow = headerRow2 + headerRow # combine the column names

    # Convert input data_highresolution to float  
    for i in range(len(data_highresolution)): # iterate over each column    
        data_highresolution[i] = list(map(float, data_highresolution[i]))  # convert data_lowresolution to float
        
# Convert input data to numpy array type
data_lowresolution = np.array(data_lowresolution)
data_highresolution = np.array(data_highresolution)

# ============= Concatenate Interpolated Data
spamWriter = csv.writer(open(outputDir + os.sep + outputFileName, 'w', newline = ''), delimiter = outputFileDelimeter) # Open csv file to write output
spamWriter.writerow(headerRow) # write the header
for i in range(0, len(data_highresolution[0])): # 0 is the col number in data_highresolution file
    value = lookupNearest(data_highresolution[0][i]) # find the row for nearest point interpolation
    for j in range(len(data_highresolution)):
        concatRow.append(data_highresolution[j][i])
    for j in range(len(data_lowresolution)):
        concatRow.append(data_lowresolution[j][value])
    spamWriter.writerow(concatRow)
    concatRow = []   

print("\n\nDONE!")