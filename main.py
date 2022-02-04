from ast import arg
from unicodedata import name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

def main():
    import argparse
    import sys
    import os
    from tabnanny import verbose

    parser = argparse.ArgumentParser()

    # Add arguments
    parser.add_argument('-path',
                        type=str,
                        help='the path to dataset')
    parser.add_argument('-m', 
                        '--mode',    
                        type=str,
                        help='c for communications engineering, d for data science mode')
    parser.add_argument("-v", 
                        "--verbose",    
                        type=int, 
                        help="increase output verbosity (1, 0)")

    # Parse arguments
    args = parser.parse_args()
    
    dataset_path = args.path
    mode=args.mode
    verbosity_level=args.verbose

    # Clean arguments

    if not os.path.isfile(dataset_path):
        print('The path specified does not exist')
        sys.exit() 

    # Execute main program 
    # Read the dataset into a pandas dataframe
    rtt_data = pd.read_csv(dataset_path) # Consider .xlsx input file format
    print('Data loaded ...\n') 
    sleep_time =3 

    time.sleep(sleep_time)

    if mode=='c' and not verbosity_level:
        comm(rtt_data, sleep_time)
        
    elif mode=='c' and verbosity_level:
        comm_v(rtt_data, sleep_time) 

    elif mode=='d' and not verbosity_level:
        dat(rtt_data, sleep_time)

    elif mode=='d' and verbosity_level:
        dat_v(rtt_data, sleep_time)

    else:
        default()
        dat_v(rtt_data, sleep_time)
        comm_v(rtt_data, sleep_time)

    




def default():
    print('Combined mode')
    

if __name__ =="__main__":
    main()
