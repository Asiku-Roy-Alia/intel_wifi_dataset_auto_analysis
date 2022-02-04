
def ReadFtmMeasFile(measFilePath): 
    import numpy as np
    import pandas as pd 
    # This function will read the data CSV file.
    # Inputs:
    # measFilePath - full path of the provided RTT_data.csv file
    # Outputs:
    # data - dataframe containing the entire dataset
    # ind - a dictionary with the indexes of each type of data in the output matrix "data"
        
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

