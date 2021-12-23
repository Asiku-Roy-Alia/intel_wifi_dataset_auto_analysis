# Copyright (C) 2018 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np
import csv
import pandas as pd 

dataset = r'E:\work\masters\Trento\Academics\Semesters\Year 1 Semester 1\146069 Next Generation Networks\project\execution\data\Data\RTT_data.csv'
def ReadFtmMeasFile(measFilePath): 
    # This function will read the data CSV file.
    # Inputs:
    # measFilePath - full path of the provided RTT_data.csv file
    # Outputs:
    # data - numeric matrix containing the entire dataset
    # ind - a utility struct with the indexes of each type of data in the output matrix "data"
        
    ## Read CSV file as matrix
    data = pd.read_csv(measFilePath) 
    
    ind = dict()
    ## Indexes of each type of data in the CSV matrix
    ind['timestamp'] = 1
    
    ind['GTpos'] = np.array([np.arange(2,4+1)])
    
    ind['ML_est_range'] = 5
    
    ind['APpos'] = np.array([np.arange(6,8+1)])
    
    ind['APnum'] = 9
    
    ind['GTrange'] = 10
    
    ind['ToDfactor'] = 11
    
    ind['channels'] = np.array([np.arange(12,467+1)])
    
    return data,ind

dat,indd=ReadFtmMeasFile(dataset) 
print(dat)